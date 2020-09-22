import React from 'react'


export const MetaList = props => {
    const {meta, delimiter='; '} = props
    const items = meta.split(delimiter).map(item => {
        const lastParen = item.lastIndexOf('(')
        const text = item.slice(0, lastParen)
        const dy = parseFloat(item.slice(lastParen + 1, -1))
        return [text, dy]
    })

    return <ul>
        {
            items.map(([text, dy]) => (
                <li key={text} style={{
                    color: dy < 0 ? 'red' : '',
                    fontWeight: Math.abs(dy) > 50 ? 'bold' : 'normal',
                }}>
                    {text} ({dy > 0 ? '+' : ''}{dy.toFixed(2)}&nbsp;&euro;)
                </li>
            ))
        }
    </ul>
}
