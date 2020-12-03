import React, { useState } from 'react'
import {
    Typography,
    Card,
    Spin,
} from 'antd'

import { LineChart } from './LineChart'
import { MetaList } from './MetaList'


const ChartCaption = ({ data, className }) => {
    const longestSeries = Math.max(
        0,
        ...data.map(series => series.data.length)
    )
    return <Typography.Title level={4} className={className}>
        {longestSeries}&nbsp;points
    </Typography.Title>
}


export const Chart = ({
    data,
    patterns,
    highlightedTags,
}) => {
    const [selectedPoint, selectPoint] = useState(null)

    return <Card
        title={<ChartCaption data={data} />}
    >
        <Spin
            spinning={data.length === 0}
            tip='Loading...'
            delay={100}
        >
            <LineChart
                data={data.concat(patterns)}
                highlightedTags={highlightedTags}
                onClick={selectPoint}
            />

            <div className='meta'>
                {
                    selectedPoint
                    && <MetaList meta={selectedPoint.data.meta} />
                }
            </div>
        </Spin>
    </Card>
}
