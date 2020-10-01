import React, { memo } from 'react'


/**
https://github.com/plouc/nivo/blob/7d52c072cc27fbb9cd1728c8127e676cb56c324a/packages/core/src/components/dots/DotsItemSymbol.js
*/
export const DotsItemSymbol = memo(props => {
    const {
        size,
        color,
        borderWidth,
        borderColor,
        datum,
        highlightedTags,
    } = props

    const shouldHighlight = datum.tags.some(
        tag => highlightedTags.indexOf(tag) >= 0
    )

    const r = shouldHighlight ? (size / 1.2) : (size / 2)
    const strokeWidth = shouldHighlight ? (borderWidth + 2) : borderWidth

    return <circle
        r={r}
        fill={color}
        stroke={borderColor}
        strokeWidth={strokeWidth}
        style={{ pointerEvents: 'none' }}
    />
})
