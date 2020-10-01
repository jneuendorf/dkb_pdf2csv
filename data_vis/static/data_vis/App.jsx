import React, { useState, useEffect } from 'react'
import styled from 'styled-components'

import { LineChart } from './LineChart'
import { TagFilter } from './TagFilter'
import { DateRange } from './DateRange'
import { MetaList } from './MetaList'
// import { intersection } from './util/set'
import { getInitialData } from './util/data'


const Container = styled.div`
    position: absolute;
    top: 5px;
    right: 5px;
    bottom: 5px;
    left: 5px;
    font-family: sans-serif;
    width: 100%;
    height: 100%;
`

const Filters = styled.div`
    position: absolute;
    top: 0;
    width: 250px;
    bottom: 0;
    left: 0;
`

const ChartContainer = styled.div`
    position: absolute;
    top: 0;
    right: 0;
    bottom: 300px;
    left: 250px;
`


export const App = props => {
    const [chartData, setChartData] = useState([])
    const [tags, setTags] = useState([])
    const [dateRangeMinMax, setDateRangeMinMax] = useState([0, 0])
    const [highlightedTags, setHighlightedTags] = useState([])
    const [selectedPoint, selectPoint] = useState(null)

    useEffect(() => {
        async function getData() {
            if (chartData.length === 0) {
                const [data, tags] = await getInitialData()
                if (data.length > 0 && tags.length > 0) {
                    setChartData(data)
                    setTags(tags)
                    // setStore({data, tags})
                    const initialDateRange = (
                        data
                        .map((series) =>
                            [series.data[0].x, series.data.slice(-1)[0].x]
                            .map(d => +Date.parse(d))
                        )
                        .reduce(([acc_start, acc_end], [current_start, current_end]) => [
                            current_start < acc_start ? current_start : acc_start,
                            current_end > acc_end ? current_end : acc_end,
                        ])
                    )
                    setDateRangeMinMax(initialDateRange)
                }
            }
        }

        getData()
    })

    return <Container>
        <Filters>
            <h3>Tags</h3>
            <TagFilter
                tags={tags}
                highlightedTags={highlightedTags}
                setHighlightedTags={setHighlightedTags}
            />
        </Filters>
        <ChartContainer>
            {
                dateRangeMinMax[0] !== dateRangeMinMax[1]
                && <DateRange
                    min={dateRangeMinMax[0]}
                    max={dateRangeMinMax[1]}
                    setChartData={setChartData}
                />
            }

            <LineChart
                data={chartData}
                highlightedTags={highlightedTags}
                onClick={selectPoint}
            />

            <div className='meta'>
                {
                    selectedPoint
                    && <MetaList meta={selectedPoint.data.meta} />
                }
            </div>
        </ChartContainer>
    </Container>

}
