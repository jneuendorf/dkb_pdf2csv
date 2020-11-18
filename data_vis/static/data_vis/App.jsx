import React, { useCallback, useState, useEffect } from 'react'
import styled from 'styled-components'

import { LineChart } from './LineChart'
import { TagFilter } from './TagFilter'
import { PatternFinders } from './PatternFinders'
import { DateRange } from './DateRange'
import { MetaList } from './MetaList'
// import { intersection } from './util/set'
import { getInitialData, associatedPatterns } from './util/data'


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
    border-right: 1px solid rgba(0,0,0,.1);
    bottom: 0;
    left: 0;
    position: absolute;
    top: 0;
    width: 250px;
`

const FilterContainer = styled.div`
    padding: 10px 5px;
    margin-bottom: 16px;
    transition: box-shadow 0.4s;

    &:hover {
        box-shadow: 0 10px 20px rgba(0,0,0,.1);
    }
`

const FilterHeading = styled.h3`
    margin-top: 5px;
`

const ChartContainer = styled.div`
    position: absolute;
    top: 0;
    right: 0;
    bottom: 200px;
    left: 250px;
`

const ChartCaption = styled(({ data, className }) => {
    const longestSeries = Math.max(
        0,
        ...data.map(series => series.data.length)
    )
    return <h4 className={className}>
        {longestSeries}&nbsp;points
    </h4>
})`
    margin: 30px 0 0 0;
    padding-left: 50px;
`


export const App = props => {
    const [chartData, setChartData] = useState([])
    const [patterns, setPatterns] = useState([])
    const [tags, setTags] = useState([])
    const [dateRangeMinMax, setDateRangeMinMax] = useState([0, 0])
    const [dateRange, setDateRange] = useState([0, 0])
    const [highlightedTags, setHighlightedTags] = useState([])
    const [selectedPoint, selectPoint] = useState(null)

    useEffect(() => {
        async function getData() {
            if (chartData.length === 0) {
                const [data, tags] = await getInitialData()
                if (data.length > 0 && tags.length > 0) {
                    setChartData(data)
                    setTags(tags)
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
                    setDateRange(initialDateRange)
                }
            }
        }

        getData()
    })

    const setDateRangeAndChartData = useCallback(
        (range, data) => {
            setDateRange(range)
            setChartData(data)
        },
        [setChartData, setDateRange],
    )
    // const applyPatterns = useCallback(
    //     patterns => setChartData(chartDataWithPatterns(patterns, chartData)),
    //     [chartData, setChartData],
    // )
    const applyPatterns = useCallback(
        patterns => setPatterns(associatedPatterns(patterns, chartData)),
        [setPatterns, chartData],
    )

    return <Container>
            <Filters>
                <FilterContainer>
                    <FilterHeading>Search</FilterHeading>
                    <input />
                </FilterContainer>
                <FilterContainer>
                    <FilterHeading>Tags</FilterHeading>
                    <TagFilter
                        tags={tags}
                        highlightedTags={highlightedTags}
                        setHighlightedTags={setHighlightedTags}
                    />
                </FilterContainer>
                <FilterContainer>
                    <PatternFinders
                        dateRange={dateRange}
                        applyPatterns={applyPatterns}
                    />
                </FilterContainer>
            </Filters>
            <ChartContainer>
                {
                    dateRangeMinMax[0] !== dateRangeMinMax[1]
                    && <DateRange
                        min={dateRangeMinMax[0]}
                        max={dateRangeMinMax[1]}
                        updateAppState={setDateRangeAndChartData}
                        setDateRangeMinMax={setDateRangeMinMax}
                    />
                }

                <ChartCaption data={chartData} />
                <LineChart
                    data={chartData.concat(patterns)}
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
