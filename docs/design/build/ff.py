"""Shared frappe-ui shell for Frappe Factory screen boards.

Every class below mirrors a frappe-ui 1.0 component or token recipe
(Button, Badge, TextInput subtle, List/ListHeader/ListRow, Tabs underline,
Sidebar/SidebarItem, PageHeader, Dialog, Switch, Checkbox, Progress).
"""
import json, os

TOKENS = open(os.path.join(os.path.dirname(__file__), 'tokens.txt')).read()

CSS = """
body{margin:0}
:root{%s;--shadow-sm:inset 0px 0.25px 1.5px 0px #ffffff29,0px 0px 1px 0px #00000033,0px 1px 3px 0px #00000024;--shadow-xl:0 0 0 1px #00000014,0 8px 24px -4px #0000001f,0 24px 48px -12px #00000029;--shadow-2xl:0 0 0 1px #00000014,0 12px 32px -6px #00000024,0 32px 64px -16px #0000002e}
.ff{height:100vh;overflow:hidden;display:flex;background:var(--surface-base);color:var(--ink-gray-8);font-family:Inter,InterVar,system-ui,sans-serif;font-size:14px;letter-spacing:.02em;line-height:1.35;-webkit-font-smoothing:antialiased}
.ff *{box-sizing:border-box}
.ff a{color:var(--ink-blue-link);text-decoration:none}
.ff a.btn{color:var(--ink-gray-8)}
.ff a.btn.solid{color:var(--ink-base)}
svg.i{width:16px;height:16px;flex:0 0 16px;fill:none;stroke:currentColor;stroke-width:1.75;stroke-linecap:round;stroke-linejoin:round}
svg.i.s35{width:14px;height:14px;flex-basis:14px}
.tab{font-variant-numeric:tabular-nums}
/* Sidebar */
.side{box-sizing:border-box;flex:0 0 14rem;width:14rem;height:100%%;overflow-y:auto;overscroll-behavior:contain;background:var(--surface-sidebar);border-right:1px solid var(--outline-gray-1);display:flex;flex-direction:column;padding:0 8px 12px}
.side-head{box-sizing:border-box;display:flex;align-items:center;gap:8px;height:40px;margin:4px 0 6px;padding:0 6px;border:0;border-radius:8px;background:transparent;text-align:left;font:inherit;cursor:pointer;width:100%%}
.side-head:hover{background:var(--surface-gray-2)}
.logo{width:28px;height:28px;flex:0 0 28px;border-radius:6px;background:var(--surface-gray-10);color:var(--ink-base);display:grid;place-items:center;font-weight:600;font-size:13px}
.si{text-decoration:none;display:flex;align-items:center;gap:8px;height:28px;padding:0 8px;border-radius:8px;color:var(--ink-gray-7)!important;font-size:14px}
.si:hover{background:var(--surface-gray-2)}
.si .i{color:var(--ink-gray-6)}
.si.on{background:var(--surface-elevation-3);box-shadow:var(--shadow-sm);color:var(--ink-gray-8)!important}
.si .lbl{flex:1;min-width:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.si .cnt{margin-right:4px;font-size:12px;color:var(--ink-gray-5);font-variant-numeric:tabular-nums}
.si .cnt.red{color:var(--ink-red-7);font-weight:500}
.slabel{display:flex;align-items:center;height:28px;padding:0 8px;margin-top:12px;font-size:13px;color:var(--ink-gray-5)}
.sgrp{display:flex;flex-direction:column;gap:2px}
.side-foot{margin-top:auto;padding:8px 8px 0;font-size:12px;color:var(--ink-gray-5);display:flex;align-items:center;gap:6px}
/* Page */
.main{flex:1 1 auto;min-width:0;min-height:0;display:flex;flex-direction:column;overflow:hidden}
.main>*:not(.ph){flex:1 1 auto;min-height:0;overflow-y:auto}
.main>.ph{flex:0 0 auto}
.panel>div{min-height:0}
.panel>div[style*="overflow:auto"]{flex:1 1 auto}
.ph{min-height:48px;display:flex;align-items:center;justify-content:space-between;gap:8px;padding:8px 20px;border-bottom:1px solid var(--outline-gray-1)}
.crumb{display:flex;align-items:center;gap:6px;font-size:18px;min-width:0;white-space:nowrap}
.crumb a{color:var(--ink-gray-5)!important;text-decoration:none}
.crumb a:hover{color:var(--ink-gray-7)!important}
.crumb .sep{color:var(--ink-gray-4)}
.crumb .cur{color:var(--ink-gray-9);font-weight:600}
.acts{display:flex;align-items:center;gap:8px}
.body{padding:20px 20px 40px;display:flex;flex-direction:column;gap:24px}
/* Buttons (sm: h-7 px-2 rounded-4 text-base) */
.btn{display:inline-flex;align-items:center;justify-content:center;gap:6px;height:28px;padding:0 8px;border:0;border-radius:8px;font:400 14px/1.15 Inter,sans-serif;letter-spacing:.02em;cursor:pointer;white-space:nowrap;color:var(--ink-gray-8);background:var(--surface-gray-2)}
.btn:hover{background:var(--surface-gray-3)}
.btn.solid{background:var(--surface-gray-10);color:var(--ink-base)}
.btn.solid:hover{background:var(--surface-gray-9)}
.btn.ghost{background:transparent}.btn.ghost:hover{background:var(--surface-gray-3)}
.btn.outline{background:var(--surface-base);border:1px solid var(--outline-gray-2)}
.btn.red{background:var(--surface-red-7);color:var(--ink-base)}
.btn.sred{background:var(--surface-red-2);color:var(--ink-red-7)}
.btn.xs{height:24px;padding:0 6px;border-radius:6px;font-size:12px}
.btn.md{height:32px;padding:0 10px}
.btn.ico{width:28px;padding:0}
.btn.xs.ico{width:24px}
.btn[disabled]{background:var(--surface-gray-2);color:var(--ink-gray-4);cursor:not-allowed}
.btn.solid[disabled]{background:var(--surface-gray-7);color:var(--ink-base)}
/* Badge (md: h-5 px-1.5 text-xs rounded-full) */
.bd{display:inline-flex;align-items:center;gap:4px;height:20px;padding:0 6px;border-radius:999px;font-size:12px;line-height:1;white-space:nowrap;font-weight:500}
.bd.sm{height:16px;padding:0 6px;font-size:11px}
.bd.gray{color:var(--ink-gray-6);background:var(--surface-gray-2)}
.bd.red{color:var(--ink-red-7);background:var(--surface-red-2)}
.bd.amber{color:var(--ink-amber-7);background:var(--surface-amber-2)}
.bd.green{color:var(--ink-green-7);background:var(--surface-green-2)}
.bd.blue{color:var(--ink-blue-7);background:var(--surface-blue-2)}
.bd.violet{color:var(--ink-violet-7);background:var(--surface-violet-2)}
.bd.s-red{color:#fff;background:var(--surface-red-7)}
.bd.s-amber{color:#fff;background:var(--surface-amber-7)}
.bd.s-gray{color:var(--ink-base);background:var(--surface-gray-10)}
.bd.o-gray{color:var(--ink-gray-6);border:1px solid var(--outline-gray-2);background:transparent}
.dot{width:6px;height:6px;flex:0 0 6px;border-radius:50%%;display:inline-block}
.dot.g{background:var(--ink-green-6, var(--ink-green-7))}.dot.r{background:var(--surface-red-7)}.dot.a{background:var(--surface-amber-6)}.dot.x{background:var(--surface-gray-6)}.dot.o{border:1.5px solid var(--ink-gray-5);background:transparent}
/* Inputs (TextInput subtle sm) */
.in{display:flex;align-items:center;gap:6px;height:28px;padding:0 8px;border-radius:8px;border:1px solid var(--surface-gray-2);background:var(--surface-gray-2);color:var(--ink-gray-8);font:400 14px Inter,sans-serif;min-width:0}
.in:hover{background:var(--surface-gray-3)}
.in.muted{color:var(--ink-gray-4)}
.in.focus{background:var(--surface-base);border-color:var(--outline-gray-4);box-shadow:var(--shadow-sm)}
.in.out{background:var(--surface-base);border-color:var(--outline-gray-2)}
.in.dis{background:var(--surface-gray-1);border-color:var(--outline-gray-1);color:var(--ink-gray-5)}
.in.err{border-color:var(--outline-red-3);background:var(--surface-base)}
.in .grow{flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.in .i{color:var(--ink-gray-5)}
.ta{min-height:72px;align-items:flex-start;padding:6px 8px;height:auto;line-height:1.5}
.fl{display:flex;flex-direction:column;gap:6px;min-width:0}
.fl>.lab{font-size:13px;color:var(--ink-gray-6)}
.fl>.lab .req{color:var(--ink-red-6, var(--ink-red-7))}
.fl>.hint{font-size:13px;color:var(--ink-gray-5);line-height:1.45}
.fl>.errm{font-size:13px;color:var(--ink-red-7)}
/* Switch sm / Checkbox */
.sw{position:relative;display:inline-flex;align-items:center;width:26px;height:16px;flex:0 0 26px;border-radius:999px;background:var(--surface-gray-4);border:2px solid transparent}
.sw::after{content:"";width:12px;height:12px;border-radius:50%%;background:var(--surface-base);box-shadow:0 1px 2px #0003}
.sw.on{background:var(--surface-gray-10);justify-content:flex-end}
.sw.dis{background:var(--surface-gray-3)}
.sw.on.dis{background:var(--surface-gray-6)}
.cb{width:16px;height:16px;flex:0 0 16px;border-radius:4px;border:1px solid var(--outline-gray-3);background:var(--surface-base);display:inline-grid;place-items:center}
.cb.on{background:var(--surface-gray-10);border-color:var(--surface-gray-10)}
.cb.on::after{content:"";width:8px;height:4px;border:2px solid #fff;border-top:0;border-right:0;transform:translateY(-1px) rotate(-45deg)}
.cb.mix{background:var(--surface-gray-10);border-color:var(--surface-gray-10)}
.cb.mix::after{content:"";width:8px;height:2px;background:#fff;border-radius:1px}
.rd{width:16px;height:16px;flex:0 0 16px;border-radius:50%%;border:1px solid var(--outline-gray-3);background:var(--surface-base);display:inline-grid;place-items:center}
.rd.on{border:5px solid var(--surface-gray-10)}
/* Tabs underline */
.tabs{display:flex;gap:16px;border-bottom:1px solid var(--outline-gray-1);padding:0 20px}
.tabs .t{display:inline-flex;align-items:center;gap:6px;height:36px;font-size:14px;color:var(--ink-gray-5);border-bottom:1px solid transparent;margin-bottom:-1px;cursor:pointer;white-space:nowrap}
.tabs .t:hover{color:var(--ink-gray-7)}
.tabs .t.on{color:var(--ink-gray-9);border-bottom-color:var(--ink-gray-9)}
.tabs .t .bd{height:16px;font-size:11px}
/* Segmented (Tabs subtle) */
.seg{display:inline-flex;padding:2px;gap:2px;border-radius:8px;background:var(--surface-gray-2)}
.seg span{display:inline-flex;align-items:center;height:24px;padding:0 10px;border-radius:6px;font-size:13px;color:var(--ink-gray-6);cursor:pointer;white-space:nowrap}
.seg span.on{background:var(--surface-elevation-3);box-shadow:var(--shadow-sm);color:var(--ink-gray-8)}
/* List (frappe-ui/list) */
.list{display:flex;flex-direction:column;margin:0 -12px}
.lh,.lr{display:grid;align-items:center;column-gap:12px;padding:0 12px}
.lh{height:32px;font-size:13px;color:var(--ink-gray-5);border-bottom:1px solid var(--outline-gray-1);white-space:nowrap}
.lh .sort{display:inline-flex;align-items:center;gap:4px;color:var(--ink-gray-7)}
.lr{min-height:44px;border-bottom:1px solid var(--outline-gray-1);font-size:14px;color:var(--ink-gray-7);cursor:pointer}
.lr:hover{background:var(--surface-gray-1)}
.lr.act{background:var(--surface-gray-3)}
.lr.sel{background:var(--surface-gray-2)}
.lr .c{min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.lr .t1{color:var(--ink-gray-8);overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.lr .t1.b{font-weight:600;color:var(--ink-gray-9)}
.lr .m{font-size:13px;color:var(--ink-gray-5);margin-top:4px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.lr .id{color:var(--ink-gray-4);font-variant-numeric:tabular-nums}
.r{text-align:right;justify-content:flex-end}
/* Card, panel, misc */
.card{border:1px solid var(--outline-gray-1);border-radius:12px;padding:16px;background:var(--surface-base);min-width:0}
.inset{background:var(--surface-gray-1);border-radius:8px;padding:10px 12px}
.h2{margin:0;font-size:16px;font-weight:600;color:var(--ink-gray-8)}
.h3{margin:0;font-size:14px;font-weight:600;color:var(--ink-gray-8)}
.qs{font-size:13px;color:var(--ink-gray-5)}
.meta{font-size:13px;color:var(--ink-gray-5)}
.p{font-size:14px;line-height:1.55;color:var(--ink-gray-7);margin:0}
.ps{font-size:13px;line-height:1.5;color:var(--ink-gray-6);margin:0}
.kpi{display:flex;flex-direction:column;gap:6px}
.kpi .k{font-size:13px;color:var(--ink-gray-5)}
.kpi .v{font-size:20px;font-weight:600;color:var(--ink-gray-9);font-variant-numeric:tabular-nums;letter-spacing:.01em}
.kpi .v small{font-size:13px;font-weight:400;color:var(--ink-gray-5)}
.kpi .d{font-size:13px;color:var(--ink-gray-5)}
.d-up{color:var(--ink-green-7)!important}.d-dn{color:var(--ink-red-7)!important}
.bar{display:block;height:4px;border-radius:99px;background:var(--surface-gray-3);overflow:hidden}
.bar>i{display:block;height:100%%;border-radius:99px;background:var(--ink-gray-7)}
.bar>i.r{background:var(--surface-red-7)}.bar>i.a{background:var(--surface-amber-6)}.bar>i.g{background:var(--surface-green-7)}
.bar.lg{height:8px}
.panel{flex:0 0 20rem;width:20rem;border-left:1px solid var(--outline-gray-1);display:flex;flex-direction:column;min-width:0}
.prow{display:grid;grid-template-columns:7.5rem minmax(0,1fr);align-items:center;gap:8px;min-height:32px;font-size:14px}
.prow>span:first-child{font-size:13px;color:var(--ink-gray-5)}
.prow>span:last-child{color:var(--ink-gray-8);min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.divy>*+*{border-top:1px solid var(--outline-gray-1)}
.alert{display:flex;gap:10px;align-items:flex-start;padding:12px 14px;border-radius:12px;border:1px solid var(--outline-gray-2);background:var(--surface-base)}
.alert .ttl{font-weight:500;color:var(--ink-gray-8)}
.alert.red .ai{color:var(--ink-red-7)}.alert.amber .ai{color:var(--ink-amber-7)}.alert.blue .ai{color:var(--ink-blue-7)}.alert.green .ai{color:var(--ink-green-7)}
.tline{position:relative;display:flex;flex-direction:column;gap:14px}
.tline .ev{display:grid;grid-template-columns:20px minmax(0,1fr);gap:8px;font-size:13px;color:var(--ink-gray-7);line-height:1.45}
.tline .ev .ic{width:20px;height:20px;border-radius:50%%;background:var(--surface-gray-2);display:grid;place-items:center;color:var(--ink-gray-6)}
.tline .ev .ic svg{width:12px;height:12px;flex-basis:12px}
.tline .ev b{font-weight:500;color:var(--ink-gray-8)}
.tline .ev .w{color:var(--ink-gray-5)}
.av{width:20px;height:20px;flex:0 0 20px;border-radius:50%%;background:var(--surface-gray-3);color:var(--ink-gray-7);font-size:10px;font-weight:600;display:inline-grid;place-items:center;letter-spacing:0}
.av.md{width:26px;height:26px;flex-basis:26px;font-size:10px}
.avs{display:inline-flex}.avs .av{border:2px solid var(--surface-base);margin-left:-6px}.avs .av:first-child{margin-left:0}
.kbd{display:inline-flex;align-items:center;height:18px;padding:0 4px;border-radius:4px;border:1px solid var(--outline-gray-2);font-size:11px;color:var(--ink-gray-6);background:var(--surface-base)}
.overlay{position:absolute;inset:0;background:#0000004d}
.dialog{position:absolute;background:var(--surface-elevation-1);border-radius:16px;box-shadow:var(--shadow-xl);overflow:hidden}
.pop{position:absolute;background:var(--surface-elevation-2);border-radius:12px;box-shadow:var(--shadow-2xl);padding:4px}
.mi{display:flex;align-items:center;gap:8px;height:28px;padding:0 8px;border-radius:8px;font-size:14px;color:var(--ink-gray-8)}
.mi.on{background:var(--surface-gray-3)}
.mi .i{color:var(--ink-gray-6)}
.toast{position:absolute;display:flex;align-items:center;gap:10px;padding:10px 12px;border-radius:10px;background:var(--surface-gray-9);color:var(--ink-base);box-shadow:var(--shadow-xl);font-size:14px}
.sel-bar{display:flex;align-items:center;gap:8px;height:40px;padding:0 6px 0 12px;border-radius:12px;background:var(--surface-base);box-shadow:var(--shadow-2xl);font-size:14px}
.chip{display:inline-flex;align-items:center;gap:6px;height:24px;padding:0 8px;border-radius:8px;background:var(--surface-gray-2);font-size:13px;color:var(--ink-gray-7);white-space:nowrap}
.chip .k{color:var(--ink-gray-5)}
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}
.grid-bg{background-image:radial-gradient(var(--outline-gray-2) 1px,transparent 1px);background-size:16px 16px}
.flow{stroke-dasharray:4 9;animation:ffflow 1.2s linear infinite}
@keyframes ffflow{to{stroke-dashoffset:-26}}
.spin{transform-box:fill-box;transform-origin:center;animation:ffspin 1.3s linear infinite}
@keyframes ffspin{to{transform:rotate(360deg)}}
.shake{animation:ffshake .25s ease-in-out infinite alternate}
@keyframes ffshake{to{transform:translateX(1px)}}
@media (prefers-reduced-motion: reduce){.ff *,.flow,.spin,.shake{animation:none!important;transition:none!important}}
""" % TOKENS

# Lucide icon inner paths (lucide.dev, ISC)
IC = {
 'grid': '<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/>',
 'factory': '<path d="M2 20a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V8l-7 5V8l-7 5V4a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2Z"/><path d="M17 18h1"/><path d="M12 18h1"/><path d="M7 18h1"/>',
 'bell': '<path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"/>',
 'bell-off': '<path d="M8.7 3A6 6 0 0 1 18 8a21.3 21.3 0 0 0 .6 5"/><path d="M17 17H3s3-2 3-9a4.67 4.67 0 0 1 .3-1.7"/><path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"/><path d="m2 2 20 20"/>',
 'octagon': '<polygon points="7.86 2 16.14 2 22 7.86 22 16.14 16.14 22 7.86 22 2 16.14 2 7.86"/><path d="M12 8v4"/><path d="M12 16h.01"/>',
 'play': '<path d="m6 3 14 9-14 9V3z"/>',
 'pause': '<rect x="14" y="4" width="4" height="16" rx="1"/><rect x="6" y="4" width="4" height="16" rx="1"/>',
 'clock': '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
 'droplet': '<path d="M12 22a7 7 0 0 0 7-7c0-2-1-3.9-3-5.5s-3.5-4-4-6.5c-.5 2.5-2 4.9-4 6.5C6 11.1 5 13 5 15a7 7 0 0 0 7 7z"/>',
 'chart': '<path d="M3 3v18h18"/><path d="m19 9-5 5-4-4-3 3"/>',
 'bars': '<path d="M3 3v18h18"/><path d="M18 17V9"/><path d="M13 17V5"/><path d="M8 17v-3"/>',
 'clipboard': '<rect x="8" y="2" width="8" height="4" rx="1"/><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><path d="M12 11h4"/><path d="M12 16h4"/><path d="M8 11h.01"/><path d="M8 16h.01"/>',
 'cpu': '<rect x="4" y="4" width="16" height="16" rx="2"/><rect x="9" y="9" width="6" height="6"/><path d="M9 1v3M15 1v3M9 20v3M15 20v3M20 9h3M20 14h3M1 9h3M1 14h3"/>',
 'layout': '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18"/><path d="M9 21V9"/>',
 'shapes': '<path d="M8.3 10a.7.7 0 0 1-.63-1.08L11.4 3a.7.7 0 0 1 1.2-.04L16.3 8.9a.7.7 0 0 1-.57 1.1Z"/><rect x="3" y="14" width="7" height="7" rx="1"/><circle cx="17.5" cy="17.5" r="3.5"/>',
 'siren': '<path d="M7 18v-6a5 5 0 1 1 10 0v6"/><path d="M5 21a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-1a2 2 0 0 0-2-2H7a2 2 0 0 0-2 2z"/><path d="M12 2v1"/>',
 'sliders': '<path d="M21 4h-7M10 4H3M21 12h-9M8 12H3M21 20h-5M12 20H3M14 2v4M8 10v4M16 18v4"/>',
 'chev-d': '<path d="m6 9 6 6 6-6"/>', 'chev-r': '<path d="m9 18 6-6-6-6"/>', 'chev-l': '<path d="m15 18-6-6 6-6"/>', 'chev-u': '<path d="m18 15-6-6-6 6"/>',
 'chevs': '<path d="m7 15 5 5 5-5"/><path d="m7 9 5-5 5 5"/>',
 'search': '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>',
 'plus': '<path d="M5 12h14"/><path d="M12 5v14"/>',
 'filter': '<path d="M3 6h18"/><path d="M7 12h10"/><path d="M10 18h4"/>',
 'check': '<path d="M20 6 9 17l-5-5"/>',
 'x': '<path d="M18 6 6 18"/><path d="m6 6 12 12"/>',
 'more': '<circle cx="12" cy="12" r="1"/><circle cx="19" cy="12" r="1"/><circle cx="5" cy="12" r="1"/>',
 'download': '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="m7 10 5 5 5-5"/><path d="M12 15V3"/>',
 'upload': '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="m17 8-5-5-5 5"/><path d="M12 3v12"/>',
 'lock': '<rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>',
 'key': '<path d="m15.5 7.5 2.3 2.3a1 1 0 0 0 1.4 0l2.1-2.1a1 1 0 0 0 0-1.4L19 4"/><path d="m21 2-9.6 9.6"/><circle cx="7.5" cy="15.5" r="5.5"/>',
 'flask': '<path d="M10 2v7.31"/><path d="M14 9.3V1.99"/><path d="M8.5 2h7"/><path d="M14 9.3a6.5 6.5 0 1 1-4 0"/><path d="M5.52 16h12.96"/>',
 'wrench': '<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>',
 'user': '<circle cx="12" cy="8" r="5"/><path d="M20 21a8 8 0 0 0-16 0"/>',
 'users': '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
 'arrow-l': '<path d="m12 19-7-7 7-7"/><path d="M19 12H5"/>',
 'arrow-r': '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
 'undo': '<path d="M9 14 4 9l5-5"/><path d="M4 9h10.5a5.5 5.5 0 0 1 5.5 5.5a5.5 5.5 0 0 1-5.5 5.5H11"/>',
 'redo': '<path d="m15 14 5-5-5-5"/><path d="M20 9H9.5A5.5 5.5 0 0 0 4 14.5A5.5 5.5 0 0 0 9.5 20H13"/>',
 'zin': '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/><path d="M11 8v6"/><path d="M8 11h6"/>',
 'zout': '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/><path d="M8 11h6"/>',
 'eye': '<path d="M2.06 12.35a1 1 0 0 1 0-.7 10.75 10.75 0 0 1 19.88 0 1 1 0 0 1 0 .7 10.75 10.75 0 0 1-19.88 0"/><circle cx="12" cy="12" r="3"/>',
 'refresh': '<path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"/><path d="M21 3v5h-5"/><path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16"/><path d="M8 16H3v5"/>',
 'info': '<circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/>',
 'alert-c': '<circle cx="12" cy="12" r="10"/><path d="M12 8v4"/><path d="M12 16h.01"/>',
 'alert-t': '<path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/><path d="M12 9v4"/><path d="M12 17h.01"/>',
 'check-c': '<circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/>',
 'circle': '<circle cx="12" cy="12" r="10"/>',
 'circle-dash': '<path d="M10.1 2.18a9.93 9.93 0 0 1 3.8 0"/><path d="M17.6 3.71a9.95 9.95 0 0 1 2.69 2.7"/><path d="M21.82 10.1a9.93 9.93 0 0 1 0 3.8"/><path d="M20.29 17.6a9.95 9.95 0 0 1-2.7 2.69"/><path d="M13.9 21.82a9.94 9.94 0 0 1-3.8 0"/><path d="M6.4 20.29a9.95 9.95 0 0 1-2.69-2.7"/><path d="M2.18 13.9a9.93 9.93 0 0 1 0-3.8"/><path d="M3.71 6.4a9.95 9.95 0 0 1 2.7-2.69"/>',
 'wifi-off': '<path d="M12 20h.01"/><path d="M8.5 16.43a5 5 0 0 1 7 0"/><path d="M5 12.86a10 10 0 0 1 5.17-2.69"/><path d="M19 12.86a10 10 0 0 0-2-1.5"/><path d="M2 8.82a15 15 0 0 1 4.17-2.65"/><path d="M10.66 5c4.01-.36 8.14.9 11.34 3.76"/><path d="m2 2 20 20"/>',
 'settings': '<path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/><circle cx="12" cy="12" r="3"/>',
 'file': '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M10 9H8"/><path d="M16 13H8"/><path d="M16 17H8"/>',
 'history': '<path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/><path d="M12 7v5l4 2"/>',
 'ext': '<path d="M15 3h6v6"/><path d="M10 14 21 3"/><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>',
 'cal': '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4"/><path d="M8 2v4"/><path d="M3 10h18"/>',
 'msg': '<path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"/>',
 'phone': '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/>',
 'zap': '<path d="M4 14a1 1 0 0 1-.78-1.63l9.9-10.2a.5.5 0 0 1 .86.46l-1.92 6.02A1 1 0 0 0 13 10h7a1 1 0 0 1 .78 1.63l-9.9 10.2a.5.5 0 0 1-.86-.46l1.92-6.02A1 1 0 0 0 11 14z"/>',
 'fuel': '<line x1="3" x2="15" y1="22" y2="22"/><line x1="4" x2="14" y1="9" y2="9"/><path d="M14 22V4a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v18"/><path d="M14 13h2a2 2 0 0 1 2 2v2a2 2 0 0 0 2 2a2 2 0 0 0 2-2V9.83a2 2 0 0 0-.59-1.42L18 5"/>',
 'package': '<path d="M11 21.73a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73z"/><path d="M12 22V12"/><path d="m3.3 7 7.703 4.734a2 2 0 0 0 1.994 0L20.7 7"/>',
 'server': '<rect width="20" height="8" x="2" y="2" rx="2"/><rect width="20" height="8" x="2" y="14" rx="2"/><line x1="6" x2="6.01" y1="6" y2="6"/><line x1="6" x2="6.01" y1="18" y2="18"/>',
 'radio': '<path d="M4.9 19.1C1 15.2 1 8.8 4.9 4.9"/><path d="M7.8 16.2c-2.3-2.3-2.3-6.1 0-8.5"/><circle cx="12" cy="12" r="2"/><path d="M16.2 7.8c2.3 2.3 2.3 6.1 0 8.5"/><path d="M19.1 4.9C23 8.8 23 15.1 19.1 19"/>',
 'gauge': '<path d="m12 14 4-4"/><path d="M3.34 19a10 10 0 1 1 17.32 0"/>',
 'link': '<path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>',
 'move': '<path d="M12 2v20"/><path d="m15 19-3 3-3-3"/><path d="m19 9 3 3-3 3"/><path d="M2 12h20"/><path d="m5 9-3 3 3 3"/><path d="m9 5 3-3 3 3"/>',
 'rotate': '<path d="M21 12a9 9 0 1 1-9-9c2.52 0 4.93 1 6.74 2.74L21 8"/><path d="M21 3v5h-5"/>',
 'pointer': '<path d="M4.04 4.04 10 21l2.5-7.5L20 11z"/>',
 'pipe': '<path d="M4 4v6a4 4 0 0 0 4 4h12"/><path d="m16 10 4 4-4 4"/>',
 'type': '<path d="M4 7V4h16v3"/><path d="M9 20h6"/><path d="M12 4v16"/>',
 'layers': '<path d="m12.83 2.18a2 2 0 0 0-1.66 0L2.6 6.08a1 1 0 0 0 0 1.83l8.58 3.91a2 2 0 0 0 1.66 0l8.58-3.9a1 1 0 0 0 0-1.83Z"/><path d="m22 12.5-8.97 4.08a2 2 0 0 1-1.66 0L2 12.5"/><path d="m22 17.5-8.97 4.08a2 2 0 0 1-1.66 0L2 17.5"/>',
 'copy': '<rect width="14" height="14" x="8" y="8" rx="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/>',
 'trash': '<path d="M3 6h18"/><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/><path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/>',
 'pen': '<path d="M12 20h9"/><path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4Z"/>',
 'sun': '<circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/>',
 'moon': '<path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/>',
 'shield': '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/>',
 'paperclip': '<path d="m21.44 11.05-9.19 9.19a6 6 0 0 1-8.49-8.49l8.57-8.57A4 4 0 1 1 18 8.84l-8.59 8.57a2 2 0 0 1-2.83-2.83l8.49-8.48"/>',
 'square': '<rect width="18" height="18" x="3" y="3" rx="2"/>',
 'grip': '<circle cx="9" cy="12" r="1"/><circle cx="9" cy="5" r="1"/><circle cx="9" cy="19" r="1"/><circle cx="15" cy="12" r="1"/><circle cx="15" cy="5" r="1"/><circle cx="15" cy="19" r="1"/>',
}

def ic(name, cls='i', style=''):
    st = f' style="{style}"' if style else ''
    return f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true"{st}>{IC[name]}</svg>'

PLANT_NAV = [
    ('Main.dc.html', 'factory', 'Plant', ''),
    ('Alarms.dc.html', 'bell', 'Alarms', '4'),
    ('Trip.dc.html', 'octagon', 'Interlock trips', '1'),
    ('QualityHold.dc.html', 'shield', 'Quality holds', '1'),
    ('Runs.dc.html', 'play', 'Production runs', ''),
    ('Downtime.dc.html', 'clock', 'Downtime', '3'),
    ('Resources.dc.html', 'droplet', 'Resources', ''),
    ('Trends.dc.html', 'chart', 'Trends', ''),
    ('Handover.dc.html', 'clipboard', 'Shift handover', ''),
]
SETUP_NAV = [
    ('Devices.dc.html', 'cpu', 'Devices and tags'),
    ('LayoutEditor.dc.html', 'layout', 'Layouts'),
    ('Symbols.dc.html', 'shapes', 'Symbol library'),
    ('AlarmDefs.dc.html', 'siren', 'Alarm definitions'),
    ('Settings.dc.html', 'sliders', 'Plant settings'),
]

COMPANY_NAV = [
    ('Dashboard.dc.html', 'gauge', 'Dashboard', ''),
    ('Plants.dc.html', 'grid', 'Plants', ''),
    ('#alarms', 'bell', 'Alarms', '6'),
    ('#trips', 'octagon', 'Interlock trips', '1'),
    ('#prod', 'play', 'Production', ''),
    ('#downtime', 'clock', 'Downtime', ''),
    ('#quality', 'shield', 'Quality holds', '1'),
    ('#maint', 'wrench', 'Maintenance', ''),
    ('#reports', 'bars', 'Reports', ''),
]
COMPANY_SETUP = [
    ('AddPlant.dc.html', 'factory', 'Plants and sites'),
    ('CompanyKiosks.dc.html', 'cpu', 'Kiosks'),
    ('Symbols.dc.html', 'shapes', 'Symbol library'),
    ('#templates', 'layers', 'Process templates'),
    ('#users', 'users', 'Users and roles'),
    ('CompanyERPNext.dc.html', 'link', 'Integrations'),
]

def _head(badge=None, title=None, sub=None, open_=False):
    st = ' style="background:var(--surface-elevation-3);box-shadow:var(--shadow-sm)"' if open_ else ''
    return ('<button type="button" class="side-head"' + st + ' aria-haspopup="menu"><span class="logo" aria-hidden="true" style="background:var(--surface-gray-10)">FF</span>'
            '<span style="display:flex;flex-direction:column;min-width:0;flex:1"><span style="font-weight:500;color:var(--ink-gray-9);line-height:1.1">Frappe Factory</span>'
            '<span style="font-size:13px;color:var(--ink-gray-7);margin-top:3px;line-height:1.1">Tunde B.</span></span>' + ic('chev-d', 'i', 'color:var(--ink-gray-5)') + '</button>')

def _plant_switch(badge, name):
    return ('<button type="button" class="si" style="height:36px;width:100%;border:1px solid var(--outline-gray-2);background:var(--surface-base);margin:2px 0 4px;font:inherit;cursor:pointer;text-align:left">'
            f'<span style="width:20px;height:20px;border-radius:5px;background:var(--surface-gray-3);color:var(--ink-gray-8);display:grid;place-items:center;font-size:10px;font-weight:600">{badge}</span>'
            f'<span class="lbl" style="font-weight:500;color:var(--ink-gray-8)">{name}</span>' + ic('chevs', 'i', 'color:var(--ink-gray-5)') + '</button>')

def _item(href, icon, label, active, cnt='', red=False):
    on = ' on' if href == active else ''
    cur = ' aria-current="page"' if on else ''
    c = f'<span class="cnt{" red" if red else ""}">{cnt}</span>' if cnt else ''
    return f'<a class="si{on}" href="{href}"{cur}>{ic(icon)}<span class="lbl">{label}</span>{c}</a>'

def sidebar(active, trip_red=True, scope='plant', plant=('K1','Koyo 1'), plant_href='Main.dc.html', counts=None, menu_open=False):
    """One sidebar component for every desktop screen. Top: the app menu (brand + user), as in Frappe CRM and Helpdesk.
    scope='company' on company screens; scope='plant' inside a plant, with a plant switcher under the app menu."""
    if scope == 'company':
        out = ['<nav class="side" aria-label="Company">', _head(open_=menu_open), '<div class="sgrp" style="margin-top:8px">']
        out += [_item(h, i, l, active, c, l == 'Interlock trips') for h, i, l, c in COMPANY_NAV]
        out.append('</div><div class="slabel">Setup</div><div class="sgrp">')
        out += [_item(h, i, l, active) for h, i, l in COMPANY_SETUP]
        out.append('</div><div class="side-foot"><span class="dot g"></span>5 plants · ERPNext linked</div></nav>')
        return '\n'.join(out)
    out = ['<nav class="side" aria-label="Plant">', _head(open_=menu_open), _plant_switch(plant[0], plant[1]),
           '<div class="slabel" style="margin-top:4px">Operate</div><div class="sgrp">']
    for href, icon, label, cnt in PLANT_NAV:
        if href == 'Main.dc.html': href = plant_href
        if counts is not None: cnt = counts.get(label, '')
        out.append(_item(href, icon, label, active, cnt, label == 'Interlock trips' and trip_red))
    out.append('</div><div class="slabel">Setup</div><div class="sgrp">')
    out += [_item(h, i, l, active) for h, i, l in SETUP_NAV]
    out.append('</div><div class="side-foot"><span class="dot g"></span>Edge online · synced 1m ago</div></nav>')
    return '\n'.join(out)

def app_menu(left=8, top=50):
    """The open app menu (frappe-ui Dropdown) with the Apps submenu, as in Frappe CRM."""
    def mi(icon, label, right='', on=False, extra=''):
        r = f'<span style="margin-left:auto;display:flex;color:var(--ink-gray-5)">{right}</span>' if right else ''
        return f'<div class="mi{" on" if on else ""}" style="font-size:14px{extra}">{icon}<span>{label}</span>{r}</div>'
    app = lambda c, t: f'<span style="width:18px;height:18px;border-radius:4px;background:{c};color:#fff;display:grid;place-items:center;font-size:9px;font-weight:700">{t}</span>'
    sep = '<div style="height:1px;background:var(--outline-gray-1);margin:4px -4px"></div>'
    main = (mi(ic('grid'), 'Apps', ic('chev-r', 'i s35'), on=True) + mi(ic('cpu'), 'Open kiosk', ic('ext', 'i s35')) + mi(ic('layout'), 'Switch to Desk', ic('ext', 'i s35')) + sep +
            mi(ic('info'), 'Help and docs') + mi(ic('moon'), 'Toggle theme') + mi(ic('settings'), 'Settings') + mi(ic('shield'), 'About') + sep + mi(ic('arrow-r'), 'Log out'))
    sub = (f'<div style="padding:4px 8px 6px;font-size:12px;color:var(--ink-gray-5)">Apps on this site</div>' +
           mi(app('oklch(0.205 0 0)', 'FF'), 'Frappe Factory', ic('check', 'i s35')) + mi(app('oklch(0.55 0.16 252)', 'E'), 'ERPNext') + mi(app('oklch(0.6 0.15 150)', 'C'), 'CRM') +
           mi(app('oklch(0.6 0.17 300)', 'H'), 'Helpdesk') + mi(app('oklch(0.55 0.15 30)', 'W'), 'WhatsApp'))
    return (f'<div class="pop" role="menu" style="left:{left}px;top:{top}px;width:212px;z-index:5">{main}</div>'
            f'<div class="pop" role="menu" style="left:{left + 216}px;top:{top}px;width:200px;z-index:5">{sub}</div>')

def crumb(*parts):
    """parts: (label, href) pairs; last is current (href None)."""
    o = ['<div class="crumb">']
    for i, (lab, href) in enumerate(parts):
        if i: o.append('<span class="sep" aria-hidden="true">/</span>')
        if href: o.append(f'<a href="{href}">{lab}</a>')
        else: o.append(f'<span class="cur">{lab}</span>')
    o.append('</div>')
    return ''.join(o)

def header(crumbs, actions=''):
    return f'<header class="ph">{crumbs}<div class="acts">{actions}</div></header>'

def page(title, body, props=None, script_vals='return {};', helmet_extra=''):
    props = props or {}
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title} · Frappe Factory</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&amp;display=swap">
<style>{CSS}{helmet_extra}</style>
</helmet>
{body}
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{json.dumps(props)}'>
class Component extends DCLogic {{
  renderVals() {{
    {script_vals}
  }}
}}
</script>
</body>
</html>
'''

def shell(active, head, content, extra_style='', scope='plant', **kw):
    return f'<div class="ff"{extra_style}>{sidebar(active, scope=scope, **kw)}<main class="main">{head}{content}</main></div>'

def write(name, html):
    p = os.path.join('/home/claude/ff-design/project', name)
    open(p, 'w').write(html)
    print('wrote', name, len(html))

def bd(text, color='gray', dot=None, cls=''):
    d = f'<span class="dot {dot}"></span>' if dot else ''
    return f'<span class="bd {color} {cls}">{d}{text}</span>'

def btn(label='', icon=None, kind='', icon_right=None, attrs=''):
    i = ic(icon) if icon else ''
    ir = ic(icon_right) if icon_right else ''
    ico = ' ico' if (icon and not label) else ''
    al = f' aria-label="{attrs}"' if (attrs and not label) else ''
    return f'<button type="button" class="btn {kind}{ico}"{al}>{i}{label}{ir}</button>'

def field(label, control, hint='', req=False, err=''):
    r = ' <span class="req">*</span>' if req else ''
    h = f'<span class="hint">{hint}</span>' if hint else ''
    e = f'<span class="errm">{err}</span>' if err else ''
    return f'<label class="fl"><span class="lab">{label}{r}</span>{control}{h}{e}</label>'

def inp(value, kind='', icon=None, right=None, ph=False):
    i = ic(icon) if icon else ''
    rr = right or ''
    c = ' muted' if ph else ''
    return f'<span class="in {kind}{c}">{i}<span class="grow">{value}</span>{rr}</span>'

def sel(value, kind='', ph=False):
    return inp(value, kind, right=ic('chev-d', 'i s35'), ph=ph)

def spark(values, w=120, h=28, color='var(--ink-gray-7)', lo=None, hi=None, lines=()):
    lo = min(values) if lo is None else lo
    hi = max(values) if hi is None else hi
    rng = (hi - lo) or 1
    pts = ' '.join(f'{i*(w/(len(values)-1)):.1f},{h-2-(v-lo)/rng*(h-4):.1f}' for i, v in enumerate(values))
    ls = ''.join(f'<line x1="0" x2="{w}" y1="{h-2-(y-lo)/rng*(h-4):.1f}" y2="{h-2-(y-lo)/rng*(h-4):.1f}" stroke="{c}" stroke-width="1" stroke-dasharray="3 3"/>' for y, c in lines)
    return f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" aria-hidden="true" style="display:block;overflow:visible">{ls}<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="1.5" stroke-linejoin="round" stroke-linecap="round"/></svg>'
