import React from 'react'


export const ToolTip = props => {
    const {point} = props
    const {data: {meta}} = point
    const [kind, recipient] = meta.split('\n')

    return <div className='tooltip' style={{maxWidth: '300px'}}>
        <div className='xy'>
            {point.data.x.toLocaleString('de-DE', {dateStyle: 'short'})}
            &nbsp;
            {point.data.y} &euro;
        </div>
        <div className='meta'>
            {kind}, {recipient}
        </div>
    </div>
}
