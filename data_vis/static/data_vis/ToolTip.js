import React from 'react'
import styled from 'styled-components'


/** See https://stackoverflow.com/a/16348977/6928824 */
const stringToRgb = str => {
    let hash = 0
    for (let i = 0; i < str.length; i++) {
        hash = str.charCodeAt(i) + ((hash << 5) - hash)
    }

    const color = []
    for (let i = 0; i < 3; i++) {
        const value = (hash >> (i * 8)) & 0xFF
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


const StyledToolTip = styled.div`
    background: rgba(255, 255, 255, 0.70);
    border: 1px solid rgba(30, 30, 30, 0.70);
    border-radius: 5px;
    max-width: 300px;
    padding: 10px;
`

const XY = ({x, y}) => <div>
    {x.toLocaleString('de-DE', {dateStyle: 'short'})}
    &nbsp; {y}
    &euro;
</div>

const StyledTag = styled.div`
    background-color: ${props => rgbToHex(stringToRgb(props.tag))};
    border-radius: 4px;
    color: ${props => colorIsLight(stringToRgb(props.tag)) ? 'black' : 'white'};
    display: inline-block;
    margin-right: 3px;
    mix-blend-mode: difference;
    padding: 4px;
`


export const ToolTip = props => {
    const {point} = props
    const {
        data: {
            meta,
            tags
        }
    } = point
    const [kind, recipient] = meta.split('\n')

    return <StyledToolTip>
        <XY x={point.data.x} y={point.data.y} />
        <div>
            {kind}, {recipient}
        </div>
        <div>
            {tags.map(
                tag => <StyledTag key={tag} tag={tag}>{tag}</StyledTag>
            )}
        </div>
    </StyledToolTip>
}
