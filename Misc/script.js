function ET(e, t) {
    const n = u.useRef(null), r = S(t, (s) => n.current = s),  // Changed from j5 to S
        {
            completionType: s,
            model: a,
            eventSource: i,
            onCreate: l,
            isCompanionWindow: c,
            isHistoryAndTrainingDisabled: d,
            currentTree: f = xe.getTree(ve(e)),
            currentNodeId: m = i,
            activeBranchLastMessage: p = f.getMessage(m),
            isCompanionWindow: c,
            completionLatencyTracker: g = new dF(p),
            turnTracker: h = new CSe(),
            isHistoryAndTrainingDisabled: i,
        } = e,
          [v, x] = u.useState(null), [b, C] = u.useState(null), w = u.useRef(null),
          M = u.useRef(!1), A = u.useRef(null),
          k = L8(() => {  // changed from H8
              if (x) {
                  const T = x[0], j = x[1], R = x[2];
                  (T === 0 || (T === 13 ? 1 : 0) || (T === 32 ? 1 : 0)) &&
                      v.currentTarget.focus();
              }
          }),
          T = u.useCallback((j) => {
              const R = j.target;
              R.hasPointerCapture(j.pointerId) && R.releasePointerCapture(j.pointerId),
                  j.button === 0 && j.ctrlKey === !1 && j.pointerType === 'mouse' &&
                      (h(j), j.preventDefault());
          }, []), j = u.useCallback((j) => {
              const R = m.current !== '';
              !(j.ctrlKey || j.altKey || j.metaKey) && j.key.length === 1 && p(j.key),
                  !(R && j.key === ' ') && Jue.includes(j.key) &&
                      (h(), j.preventDefault());
          }, [p, h]), R = wI(arguments, {});
    let N = null;
    const O = o.jsxs('button', {
        type: 'button',
        role: 'switch',
        'aria-checked': b,
        'aria-required': i,
        'data-state': IC(b),
        'data-disabled': l ? '' : void 0,
        disabled: l,
        value: c,
        ...m,
        ref: h,
        onClick: pe(e.onClick,
                    (v) => {
                        v.currentTarget.focus(), f.current !== 'mouse' && h(v);
                    }),
        onPointerDown: pe(e.onPointerDown, T),
        onKeyDown: pe(e.onKeyDown, j),
        'data-testid': s === 'streaming' ? 'stop-button' :
                                           'send-button'  // Key change here!
    });

    return o.jsxs('div', {
        'data-testid': `bar-${f?.name ?? 'default'}`,
        className: P('grid gap-bar', t === 'vertical' && 'flex-col',
                     a && [Ko.leadingBar, Ko.leadingBarScrollAnimation],
                     i && [Ko.trailingBar, Ko.trailingBarScrollAnimation],
                     d === 'primary' && Ko.primary, r),
        ref: l ?? p,
        style: {...c, ...m, ...h, ...x, ...C},
        children: [
            o.jsx('div', {
                slot: 'leading',
                ref: b,
                children: a,
            }),
            o.jsx('div', {
                slot: 'content',
                className: s,
                children: o.jsxs('div', {
                    className: P(
                        'text-message flex w-full flex-col items-end gap-2 whitespace-normal break-words text-start [.text-message+&]:mt-5'),
                    'data-message-model-slug': p[0].message.metadata?.model_slug,
                    'data-message-author-role': p[0].message.author.role,
                    'data-message-id': p[0].message.id,
                    dir: 'auto',
                    children: [
                        n && o.jsx(Ioe, {
                            clientThreadId: s,
                            groupedMessages: r,
                        }),
                        o.jsx(Mle, {messages: p}), !1, o.jsx(Fle, {messages: p}),
                        o.jsx(gwe, {
                            messages: p,
                            isActivelyStreaming: c,
                            isUserTurn: d,
                            displayParts: g,
                            turnIndex: f,
                            clientThreadId: m,
                            id: p[0].nodeId,
                            isFeedbackEnabled: i,
                            prevGroupedMessageType: h,
                            prevGroupedMessages: v,
                            showEditButton: x,
                            onEnterEdit: b
                        }),
                        o.jsx(xce, {
                            message: w ? void 0 : p[0],
                            id: p[0].nodeId,
                            isFeedbackEnabled: i,
                            clientThreadId: s,
                            isUserTurn: d
                        }),
                        o.jsx(Vle, {isUserTurn: d, message: w ? void 0 : p[0]}),
                        !d && !c && v && h === ie.SearchResult &&
                            o.jsx(Oce, {messages: v})
                    ]
                })

            }),
            o.jsx('div', {
                slot: 'trailing',
                ref: (j) => {
                    w(j), (k.current = j);
                },
                children: i,
            }),
        ],
    });
}