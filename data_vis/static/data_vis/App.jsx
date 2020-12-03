import React, { useCallback, useState, useEffect } from 'react'
import {
    Layout,
    Collapse,
} from 'antd'

import { TagFilter } from './TagFilter'
import { PatternFinders } from './PatternFinders'
import { DateRange } from './DateRange'
import { Chart } from './Chart'
import { getInitialData, associatedPatterns } from './util/data'


const {
    Content,
 } = Layout


const Sider = (props) => {
    const [collapsed, setCollapsed] = useState(false)
    return <Layout.Sider
        {...props}
        collapsible
        collapsed={collapsed}
        onCollapse={useCallback(
            (collapsed) => setCollapsed(collapsed),
            [setCollapsed]
        )}
        theme="light"
        width={250}
    />
}


export const App = props => {
    const [chartData, setChartData] = useState([])
    const [patterns, setPatterns] = useState([])
    const [tags, setTags] = useState([])
    const [dateRangeMinMax, setDateRangeMinMax] = useState([0, 0])
    const [dateRange, setDateRange] = useState([0, 0])
    const [highlightedTags, setHighlightedTags] = useState([])

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

    return <Layout>
        <Sider>
            <Collapse defaultActiveKey={['search', 'tags', 'patternFinders']}>
                <Collapse.Panel key='search' header='Search'>
                    <input />
                </Collapse.Panel>
                <Collapse.Panel key='tags' header='Tags'>
                    <TagFilter
                        tags={tags}
                        highlightedTags={highlightedTags}
                        setHighlightedTags={setHighlightedTags}
                    />
                </Collapse.Panel>
                <Collapse.Panel key='patternFinders' header='Patterns'>
                    <PatternFinders
                        dateRange={dateRange}
                        applyPatterns={applyPatterns}
                    />
                </Collapse.Panel>
            </Collapse>
        </Sider>
        <Layout>
            <Content>
                {
                    dateRangeMinMax[0] !== dateRangeMinMax[1]
                    && <DateRange
                        min={dateRangeMinMax[0]}
                        max={dateRangeMinMax[1]}
                        updateAppState={setDateRangeAndChartData}
                        setDateRangeMinMax={setDateRangeMinMax}
                    />
                }
                <Chart
                    data={chartData}
                    patterns={patterns}
                    highlightedTags={highlightedTags}
                />
            </Content>
        </Layout>
    </Layout>
}
