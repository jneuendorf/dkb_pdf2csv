import React, { useState, useEffect } from 'react'

import { MyResponsiveLine } from './LineChart'
import { MetaList } from './MetaList'


export const App = props => {
    const [data, setData] = useState(null)
    const [selectedPoint, selectPoint] = useState(null)

    const {search} = new URL(window.location.href)

    useEffect(() => {
        async function getData() {
            if (!data) {
                const response = await fetch(`/data_vis/api/${search}`)
                const data = await response.json()
                setData(data)
                console.log(data)
            }
        }

        getData()
    })

    return <div style={{
        position: 'absolute',
        top: '80px',
        right: '150px',
        bottom: '300px',
        left: '150px',
    }}>
        <MyResponsiveLine data={data} onClick={selectPoint} />
        <div className='meta'>
            {
                selectedPoint
                && <MetaList meta={selectedPoint.data.meta} />
            }
        </div>
    </div>
}
