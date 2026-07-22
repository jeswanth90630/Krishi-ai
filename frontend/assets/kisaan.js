/**
 * KISAAN — Krishi AI Smart Agricultural Chatbot
 * Premium AI Farming Advisor (Chat Only)
 * Bottom-Right Floating FAB
 */
(function () {
    'use strict';

    const KISAAN = {
        isOpen: false,
        history: [],
        pageContext: document.title.replace(' - Krishi AI', '').trim(),

        inject() {
            this._injectStyles();
            this._injectChatWidget();
            this._bindEvents();
        },

        _injectStyles() {
            if (document.getElementById('__kisaan_css__')) return;
            const s = document.createElement('style');
            s.id = '__kisaan_css__';
            s.textContent = `
                /* ── Floating FAB (Bottom-Right) ── */
                #kisaan-fab {
                    position: fixed;
                    bottom: 25px;
                    right: 25px;
                    z-index: 10000;
                    width: 64px; height: 64px;
                    border-radius: 50%;
                    background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%);
                    border: none; cursor: pointer;
                    box-shadow: 0 8px 32px rgba(0,242,254,0.45), 0 0 0 0 rgba(0,242,254,0.25);
                    display: flex; align-items: center; justify-content: center;
                    font-size: 1.8rem;
                    transition: all 0.3s cubic-bezier(0.175,0.885,0.32,1.275);
                    animation: kisaan_pulse_fab 3s infinite;
                }
                #kisaan-fab:hover { transform: scale(1.1) translateY(-2px); box-shadow: 0 10px 40px rgba(0,242,254,0.6); }
                #kisaan-fab.active { background: linear-gradient(135deg, #ff5e5e, #ff9a3c); animation: none; transform: rotate(90deg); }

                @keyframes kisaan_pulse_fab {
                    0%, 100% { box-shadow: 0 8px 32px rgba(0,242,254,0.45), 0 0 0 0 rgba(0,242,254,0.25); }
                    50%      { box-shadow: 0 8px 32px rgba(0,242,254,0.45), 0 0 0 15px rgba(0,242,254,0); }
                }

                /* ── Chat Window ── */
                #kisaan-window {
                    position: fixed;
                    bottom: 105px;
                    right: 25px;
                    width: 400px;
                    height: 580px;
                    background: rgba(10,15,28,0.92);
                    backdrop-filter: blur(22px);
                    -webkit-backdrop-filter: blur(22px);
                    border: 1px solid rgba(0,242,254,0.25);
                    border-radius: 28px;
                    display: flex; flex-direction: column;
                    overflow: hidden;
                    box-shadow: 0 30px 90px rgba(0,0,0,0.8);
                    transform: scale(0.9) translateY(40px);
                    opacity: 0;
                    pointer-events: none;
                    transition: all 0.4s cubic-bezier(0.34,1.56,0.64,1);
                    z-index: 10001;
                }
                #kisaan-window.open {
                    transform: scale(1) translateY(0);
                    opacity: 1;
                    pointer-events: all;
                }

                #kisaan-header {
                    padding: 20px 24px;
                    background: linear-gradient(135deg, rgba(0,242,254,0.12), rgba(79,172,254,0.06));
                    border-bottom: 1px solid rgba(0,242,254,0.18);
                    display: flex; align-items: center; gap: 14px;
                }
                #kisaan-header-icon {
                    width: 46px; height: 46px; border-radius: 50%;
                    background: linear-gradient(135deg, #00f2fe, #4facfe);
                    display: flex; align-items: center; justify-content: center;
                    font-size: 1.45rem; box-shadow: 0 0 20px rgba(0,242,254,0.35);
                }
                #kisaan-header-info h4 { margin: 0; font-family: 'Outfit', sans-serif; font-weight: 800; font-size: 1.1rem; color: #fff; letter-spacing: 0.5px; }
                #kisaan-header-info p { margin: 0; font-size: 0.75rem; color: #64748b; margin-top: 2px; }

                #kisaan-messages {
                    flex: 1; overflow-y: auto; padding: 22px;
                    display: flex; flex-direction: column; gap: 18px;
                }
                #kisaan-messages::-webkit-scrollbar { width: 4px; }
                #kisaan-messages::-webkit-scrollbar-thumb { background: rgba(0,242,254,0.2); border-radius: 2px; }

                .k-msg { display: flex; gap: 12px; animation: k-in 0.3s ease; }
                @keyframes k-in { from{transform:translateY(10px);opacity:0} to{transform:translateY(0);opacity:1} }
                .k-msg.user { flex-direction: row-reverse; }

                .k-bubble {
                    max-width: 82%; padding: 12px 18px; border-radius: 20px;
                    font-family: 'Outfit', sans-serif; font-size: 0.9rem; line-height: 1.55;
                }
                .k-msg.bot .k-bubble {
                    background: rgba(255,255,255,0.05); color: #e2e8f0; border-bottom-left-radius: 4px; border: 1px solid rgba(255,255,255,0.08);
                }
                .k-msg.user .k-bubble {
                    background: linear-gradient(135deg, rgba(0,242,254,0.22), rgba(79,172,254,0.18)); color: #fff; border-bottom-right-radius: 4px; border: 1px solid rgba(0,242,254,0.3);
                }

                #kisaan-input-wrap {
                    padding: 18px; background: rgba(0,0,0,0.3);
                    border-top: 1px solid rgba(0,242,254,0.12);
                    display: flex; gap: 12px; align-items: flex-end;
                }
                #kisaan-input {
                    flex: 1; background: rgba(255,255,255,0.06);
                    border: 1px solid rgba(255,255,255,0.12);
                    border-radius: 16px; color: #fff; padding: 14px 18px;
                    font-family: 'Outfit', sans-serif; font-size: 0.92rem;
                    outline: none; resize: none; max-height: 100px;
                    transition: border-color 0.2s;
                }
                #kisaan-input:focus { border-color: rgba(0,242,254,0.45); }
                #kisaan-send {
                    width: 48px; height: 48px; border-radius: 16px;
                    background: linear-gradient(135deg, #00f2fe, #4facfe);
                    border: none; cursor: pointer; display: flex; align-items: center; justify-content: center;
                    font-size: 1.2rem; transition: 0.2s;
                }
                #kisaan-send:hover { transform: scale(1.06); filter: brightness(1.1); }
                #kisaan-send:disabled { opacity: 0.5; cursor: not-allowed; }

                .k-typing { display: flex; gap: 5px; padding: 4px 0; }
                .k-dot { width: 6px; height: 6px; border-radius: 50%; background: #00f2fe; animation: k-dots 1.4s infinite; opacity: 0.4; }
                .k-dot:nth-child(2) { animation-delay: 0.2s; }
                .k-dot:nth-child(3) { animation-delay: 0.4s; }
                @keyframes k-dots { 0%,100%{opacity:0.3;transform:scale(0.8)} 50%{opacity:1;transform:scale(1.1)} }

                @media (max-width: 480px) {
                    #kisaan-window { width: calc(100vw - 32px); right: 16px; bottom: 100px; height: 70vh; }
                }
            `;
            document.head.appendChild(s);
        },

        _injectChatWidget() {
            const fab = document.createElement('button');
            fab.id = 'kisaan-fab';
            fab.innerHTML = '🌾';
            fab.title = 'Speak with Kisaan AI Advisor';
            document.body.appendChild(fab);

            const win = document.createElement('div');
            win.id = 'kisaan-window';
            win.innerHTML = `
                <div id="kisaan-header">
                    <div id="kisaan-header-icon">🌾</div>
                    <div id="kisaan-header-info" style="flex:1">
                        <h4>Kisaan</h4>
                        <p>Universal Farming Advisor · Online</p>
                    </div>
                    <button id="kisaan-close" style="background:none;border:none;color:#64748b;font-size:1.4rem;cursor:pointer;padding:4px;">✕</button>
                </div>
                <div id="kisaan-messages"></div>
                <div id="kisaan-input-wrap">
                    <textarea id="kisaan-input" rows="1" placeholder="Describe your farm issue..."></textarea>
                    <button id="kisaan-send">➤</button>
                </div>
            `;
            document.body.appendChild(win);

            this._addBotMessage("Namaste! 🌾 I am Kisaan, your personal agricultural AI. I can guide you on soil health, pest control, and yield growth! Ask me anything.");
        },

        _bindEvents() {
            document.getElementById('kisaan-fab').onclick = () => this.toggleChat();
            document.getElementById('kisaan-close').onclick = () => this.toggleChat();
            document.getElementById('kisaan-send').onclick = () => this.sendMessage();
            document.getElementById('kisaan-input').onkeydown = (e) => {
                if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); this.sendMessage(); }
            };
            const input = document.getElementById('kisaan-input');
            input.oninput = () => {
                input.style.height = 'auto';
                input.style.height = Math.min(input.scrollHeight, 100) + 'px';
            };
        },

        toggleChat() {
            this.isOpen = !this.isOpen;
            document.getElementById('kisaan-window').classList.toggle('open', this.isOpen);
            document.getElementById('kisaan-fab').classList.toggle('active', this.isOpen);
            document.getElementById('kisaan-fab').innerHTML = this.isOpen ? '✕' : '🌾';
            if(this.isOpen) document.getElementById('kisaan-input').focus();
        },

        async sendMessage() {
            const input = document.getElementById('kisaan-input');
            const text = input.value.trim();
            if(!text) return;
            input.value = '';
            input.style.height = 'auto';

            this._addUserMessage(text);
            this.history.push({role: 'user', content: text});

            const typingId = this._addTyping();
            try {
                const res = await fetch('/api/chat/', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        message: text,
                        page_context: this.pageContext,
                        history: this.history.slice(-8),
                        lang: 'en' // Hardcoded to English since translation is removed
                    })
                });
                const data = await res.json();
                this._removeTyping(typingId);
                const reply = data.reply || "I am thinking. Please ask again!";
                this._addBotMessage(reply);
                this.history.push({role: 'assistant', content: reply});
            } catch (err) {
                this._removeTyping(typingId);
                this._addBotMessage("I cannot reach the field satellites. Please check your internet! 🌱");
            }
        },

        _addUserMessage(t) {
            const m = document.getElementById('kisaan-messages');
            const d = document.createElement('div');
            d.className = 'k-msg user';
            d.innerHTML = `<div class="k-bubble">${this._escape(t)}</div>`;
            m.appendChild(d);
            m.scrollTop = m.scrollHeight;
        },

        _addBotMessage(t) {
            const m = document.getElementById('kisaan-messages');
            const d = document.createElement('div');
            d.className = 'k-msg bot';
            const fmt = t.replace(/\*\*(.*?)\*\*/g, '<strong style="color:#00f2fe">$1</strong>').replace(/\n/g, '<br>');
            d.innerHTML = `<div class="k-bubble">${fmt}</div>`;
            m.appendChild(d);
            m.scrollTop = m.scrollHeight;
        },

        _addTyping() {
            const m = document.getElementById('kisaan-messages');
            const id = 't_' + Date.now();
            const d = document.createElement('div');
            d.id = id; d.className = 'k-msg bot';
            d.innerHTML = `<div class="k-bubble"><div class="k-typing"><div class="k-dot"></div><div class="k-dot"></div><div class="k-dot"></div></div></div>`;
            m.appendChild(d);
            m.scrollTop = m.scrollHeight;
            return id;
        },

        _removeTyping(id) {
            const el = document.getElementById(id);
            if(el) el.remove();
        },

        _escape(s) {
            return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
        }
    };

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => KISAAN.inject());
    } else {
        KISAAN.inject();
    }
})();
