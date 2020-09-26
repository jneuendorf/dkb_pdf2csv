import React from 'react'

/** See https://stackoverflow.com/a/16348977/6928824 */
const stringToRgb = str => {
    let hash = 0
    for (let i = 0; i < str.length; i++) {
        hash = str.charCodeAt(i) + ((hash << 5) - hash)
    }

    // let color = '#'
    const color = []
    for (let i = 0; i < 3; i++) {
        const value = (hash >> (i * 8)) & 0xFF
        // color += ('00' + value.toString(16)).substr(-2)
        color[i] = value
    }
    return color
}

const rgbToHex = ([r, g, b]) => {
    return (
        '#'
        + ('00' + r.toString(16)).substr(-2)
        + ('00' + g.toString(16)).substr(-2)
        + ('00' + b.toString(16)).substr(-2)
    )
}

/** See https://stackoverflow.com/a/41042412/6928824 */
const colorIsLight = ([r, g, b]) => {
    // Counting the perceptive luminance human eye favors green color...
    const a = 1 - (0.299 * r + 0.587 * g + 0.114 * b) / 255
    return a < 0.5
}


export const ToolTip = props => {
    const {point} = props
    const {
        data: {
            meta,
            tags
        }
    } = point
    const [kind, recipient] = meta.split('\n')

    return <div className='tooltip' style={{
            background: 'rgba(255, 255, 255, 0.70)',
            border: '1px solid rgba(30, 30, 30, 0.70)',
            borderRadius: '5px',
            maxWidth: '300px',
            padding: '10px'
        }}>
        <div className='xy'>
            {point.data.x.toLocaleString('de-DE', {dateStyle: 'short'})}
            &nbsp; {point.data.y}
            &euro;
        </div>
        <div className='meta'>
            {kind}, {recipient}
        </div>
        <div className='tags'>
            {
                tags.map(tag => <div key={tag} className='tag' style={{
                    backgroundColor: rgbToHex(stringToRgb(tag)),
                    borderRadius: '4px',
                    color: colorIsLight(stringToRgb(tag)) ? 'black' : 'white',
                    display: 'inline-block',
                    marginRight: '3px',
                    mixBlendMode: 'difference',
                    padding: '4px',
                }}>
                    {tag}
                </div>)
            }
        </div>
    </div>
}
