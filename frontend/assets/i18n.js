/**
 * Krishi AI — Full-Page Auto Translation Engine
 * Uses Gemini API (via backend) to translate every visible text node on the page.
 * Language is persisted in localStorage and applied on every page load.
 */
const i18n = {
    currentLang: localStorage.getItem('krishi_lang') || 'en',

    // Persistent cache in localStorage: { pageName_lang: { originalText: translatedText } }
    _cache: JSON.parse(localStorage.getItem('krishi_cache') || '{}'),

    // Tags whose subtrees should be entirely skipped (e.g. scripts, models, canvases)
    SKIP_SUBTREE: new Set(['SCRIPT', 'STYLE', 'LINK', 'HEAD', 'NOSCRIPT', 'IFRAME', 'CODE', 'PRE', 'CANVAS', 'VIDEO', 'AUDIO', 'MODEL-VIEWER']),

    // Tags that are leaf elements or we only want attributes from them (don't walk inside)
    LEAF_TAGS: new Set(['INPUT', 'SELECT', 'TEXTAREA', 'OPTION', 'IMG', 'BUTTON']),

    // Attrs to also translate
    TRANSLATE_ATTRS: ['placeholder', 'title', 'alt'],

    /**
     * Main entry — called on DOMContentLoaded.
     * Injects the language pill, then if lang != 'en', translates the page.
     */
    async init() {
        this.injectDropdown();

        if (this.currentLang !== 'en') {
            await this.translatePage();
        }
    },

    /**
     * Called when a user picks a language from the dropdown.
     */
    async setLang(lang) {
        this.currentLang = lang;
        localStorage.setItem('krishi_lang', lang);
        this.injectDropdown(); // Re-render to show selected

        if (lang === 'en') {
            // Reload to restore original English DOM
            location.reload();
            return;
        }

        await this.translatePage();
    },

    /**
     * Core translator: collect all visible text, batch-send to Gemini, apply translations.
     */
    async translatePage() {
        const lang = this.currentLang;
        const pageKey = window.location.pathname.split('/').pop() || 'index';
        const cacheKey = `${pageKey}_${lang}`;

        // Check cache first
        if (this._cache[cacheKey]) {
            this._applyTranslations(this._cache[cacheKey]);
            return;
        }

        // Show subtle loading overlay
        const overlay = this._showLoadingOverlay(lang);

        try {
            // Collect all text nodes and translatable attributes
            const textNodeMap = []; // { node, original }
            const attrNodeMap = []; // { el, attr, original }

            this._walkDOM(document.body, textNodeMap, attrNodeMap);

            // Deduplicate texts
            const uniqueTexts = [...new Set([
                ...textNodeMap.map(n => n.original),
                ...attrNodeMap.map(a => a.original)
            ])].filter(t => t && t.trim().length > 1);

            if (uniqueTexts.length === 0) {
                overlay.remove();
                return;
            }

            // Send to backend for Gemini translation
            const response = await fetch('/api/translate/page', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ texts: uniqueTexts, lang })
            });

            if (!response.ok) throw new Error('Translation API failed');

            const data = await response.json();
            const translations = data.translations || {};

            // Cache it
            this._cache[cacheKey] = translations;
            localStorage.setItem('krishi_cache', JSON.stringify(this._cache));

            // Apply
            this._applyTranslations(translations, textNodeMap, attrNodeMap);

        } catch (err) {
            console.warn('Krishi i18n: Translation failed —', err.message);
        } finally {
            overlay.remove();
        }
    },

    /**
     * Walk the DOM and collect text nodes + translatable attributes.
     */
    _walkDOM(root, textNodeMap, attrNodeMap) {
        const walker = document.createTreeWalker(
            root,
            NodeFilter.SHOW_TEXT | NodeFilter.SHOW_ELEMENT,
            {
                acceptNode: (node) => {
                    const tag = node.tagName;
                    
                    // Reject the floating language pill entirely
                    if (node.nodeType === Node.ELEMENT_NODE && node.closest('.lang-floating-pill')) {
                        return NodeFilter.FILTER_REJECT;
                    }

                    // Reject scripts, styles, etc. and their children
                    if (this.SKIP_SUBTREE.has(tag)) {
                        return NodeFilter.FILTER_REJECT;
                    }

                    // For text nodes, only accept if they have meaningful content
                    if (node.nodeType === Node.TEXT_NODE) {
                        const text = node.textContent.trim();
                        if (!text || text.length < 2) return NodeFilter.FILTER_REJECT;
                        // Skip pure numbers/symbols
                        if (/^[\d\s%°+\-–—.,:;/()[\]{}|]*$/.test(text)) return NodeFilter.FILTER_REJECT;
                        return NodeFilter.FILTER_ACCEPT;
                    }

                    // For element nodes, always accept so we can check attributes
                    return NodeFilter.FILTER_ACCEPT;
                }
            }
        );

        let currentNode = walker.nextNode();
        while (currentNode) {
            if (currentNode.nodeType === Node.TEXT_NODE) {
                const original = currentNode.textContent.trim();
                textNodeMap.push({ node: currentNode, original });
            } else if (currentNode.nodeType === Node.ELEMENT_NODE) {
                // Check translatable attributes first
                for (const attr of this.TRANSLATE_ATTRS) {
                    const val = currentNode.getAttribute(attr);
                    if (val && val.trim().length > 1) {
                        attrNodeMap.push({ el: currentNode, attr, original: val.trim() });
                    }
                }
                
                // If it's a leaf tag, we don't need to look at its "text" children (if any)
                if (this.LEAF_TAGS.has(currentNode.tagName)) {
                    // Manual skip over children if necessary, but TreeWalker will 
                    // continue to its children unless we return reject.
                }
            }
            currentNode = walker.nextNode();
        }
    },

    /**
     * Apply the translations map to the DOM.
     * If textNodeMap/attrNodeMap are not passed, do a fresh walk.
     */
    _applyTranslations(translations, textNodeMap, attrNodeMap) {
        if (!textNodeMap) {
            textNodeMap = [];
            attrNodeMap = [];
            this._walkDOM(document.body, textNodeMap, attrNodeMap);
        }

        for (const { node, original } of textNodeMap) {
            if (translations[original]) {
                // Preserve surrounding whitespace
                const before = node.textContent.match(/^\s*/)[0];
                const after = node.textContent.match(/\s*$/)[0];
                node.textContent = before + translations[original] + after;
            }
        }

        for (const { el, attr, original } of attrNodeMap) {
            if (translations[original]) {
                el.setAttribute(attr, translations[original]);
            }
        }
    },

    /**
     * Show a slim translucent loading bar at the top.
     */
    _showLoadingOverlay(lang) {
        const langLabels = { hi: 'हिंदी', te: 'తెలుగు', en: 'English' };
        const bar = document.createElement('div');
        bar.id = '__i18n_loading__';
        bar.style.cssText = `
            position: fixed;
            top: 0; left: 0; right: 0;
            height: 3px;
            background: linear-gradient(90deg, #00f2fe, #4facfe, #a8ff78);
            background-size: 200% 100%;
            animation: i18n_slide 1.2s linear infinite;
            z-index: 99999;
        `;

        // Toast notification
        const toast = document.createElement('div');
        toast.style.cssText = `
            position: fixed;
            bottom: 25px; right: 25px;
            background: rgba(5, 11, 20, 0.92);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(0, 242, 254, 0.3);
            border-radius: 14px;
            padding: 14px 20px;
            color: #fff;
            font-family: 'Outfit', sans-serif;
            font-size: 0.88rem;
            font-weight: 600;
            z-index: 99999;
            display: flex;
            align-items: center;
            gap: 10px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.5);
            animation: i18n_fadein 0.3s ease;
        `;
        toast.innerHTML = `🌐 <span>Converting to <b style="color:#00f2fe">${langLabels[lang]}</b>...</span>`;

        // Inject keyframes
        if (!document.getElementById('__i18n_style__')) {
            const style = document.createElement('style');
            style.id = '__i18n_style__';
            style.textContent = `
                @keyframes i18n_slide { 0%{background-position:0 0} 100%{background-position:200% 0} }
                @keyframes i18n_fadein { from{opacity:0;transform:translateY(10px)} to{opacity:1;transform:translateY(0)} }
            `;
            document.head.appendChild(style);
        }

        document.body.appendChild(bar);
        document.body.appendChild(toast);

        // Return a combined remove handle
        return { remove: () => { bar.remove(); toast.remove(); } };
    },

    /**
     * Inject the floating language pill (fixed position, top-right, non-intrusive).
     */
    injectDropdown() {
        const existing = document.querySelector('.lang-floating-pill');
        if (existing) existing.remove();

        const langLabels = { en: '🌐 English', hi: '🌐 हिंदी', te: '🌐 తెలుగు' };

        const pill = document.createElement('div');
        pill.className = 'lang-floating-pill';
        pill.style.cssText = `
            position: fixed;
            top: 20px;
            right: 22px;
            z-index: 10000;
            background: rgba(5, 11, 20, 0.75);
            backdrop-filter: blur(18px);
            -webkit-backdrop-filter: blur(18px);
            border: 1px solid rgba(0, 242, 254, 0.25);
            padding: 7px 16px 7px 12px;
            border-radius: 50px;
            display: flex;
            align-items: center;
            gap: 8px;
            box-shadow: 0 4px 24px rgba(0, 0, 0, 0.45), 0 0 0 1px rgba(0,242,254,0.05);
            transition: all 0.25s ease;
            cursor: pointer;
            font-family: 'Outfit', sans-serif;
        `;

        pill.innerHTML = `
            <select onchange="i18n.setLang(this.value)" style="
                background: none;
                border: none;
                color: #e0f7ff;
                font-family: 'Outfit', sans-serif;
                font-size: 0.82rem;
                font-weight: 700;
                cursor: pointer;
                outline: none;
                appearance: none;
                padding-right: 22px;
                letter-spacing: 0.3px;
                background-image: url('data:image/svg+xml;charset=US-ASCII,%3Csvg width%3D%2210%22 height%3D%226%22 viewBox%3D%220 0 10 6%22 fill%3D%22none%22 xmlns%3D%22http%3A//www.w3.org/2000/svg%22%3E%3Cpath d%3D%22M1 1L5 5L9 1%22 stroke%3D%2200f2fe%22 stroke-width%3D%221.5%22 stroke-linecap%3D%22round%22 stroke-linejoin%3D%22round%22/%3E%3C/svg%3E');
                background-repeat: no-repeat;
                background-position: right 0px center;
            ">
                <option value="en" ${this.currentLang === 'en' ? 'selected' : ''} style="background:#050b14; color:#fff;">🌐 English</option>
                <option value="hi" ${this.currentLang === 'hi' ? 'selected' : ''} style="background:#050b14; color:#fff;">🌐 हिंदी</option>
                <option value="te" ${this.currentLang === 'te' ? 'selected' : ''} style="background:#050b14; color:#fff;">🌐 తెలుగు</option>
            </select>
        `;

        pill.addEventListener('mouseover', () => {
            pill.style.background = 'rgba(0, 242, 254, 0.12)';
            pill.style.borderColor = 'rgba(0, 242, 254, 0.55)';
            pill.style.boxShadow = '0 4px 24px rgba(0,0,0,0.45), 0 0 12px rgba(0,242,254,0.2)';
            pill.style.transform = 'translateY(-1px)';
        });
        pill.addEventListener('mouseout', () => {
            pill.style.background = 'rgba(5, 11, 20, 0.75)';
            pill.style.borderColor = 'rgba(0, 242, 254, 0.25)';
            pill.style.boxShadow = '0 4px 24px rgba(0, 0, 0, 0.45), 0 0 0 1px rgba(0,242,254,0.05)';
            pill.style.transform = 'translateY(0)';
        });

        document.body.appendChild(pill);
    }
};

document.addEventListener('DOMContentLoaded', () => i18n.init());
