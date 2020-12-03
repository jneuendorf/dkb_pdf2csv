import React, { useState, useCallback } from 'react'
import { Slider } from 'antd'
import styled from 'styled-components'

import { updateChartData } from './util/data'
import { toShortIsoString } from './util/date'


const DateRangeContainer = styled.div`
    padding: 10px 50px;
`


export const DateRange = ({ min, max, updateAppState, setDateRangeMinMax }) => {
    const [dateRange, setDateRange] = useState([min, max])
    // Minus one quarter
    const decreaseMin = useCallback(
        () => setDateRangeMinMax([min - (365.25/4)*24*3600*1000, max]),
        [min, setDateRangeMinMax]
    )
    const applyDateRange = useCallback(
        range => updateChartData(range, updateAppState),
        [updateAppState],
    )

    return <DateRangeContainer>
        <button onClick={decreaseMin}>&lt;</button>
        <Slider
            range
            min={min}
            max={max}
            value={dateRange}
            onChange={setDateRange}
            onAfterChange={applyDateRange}
            step={24 * 60 * 60 * 1000}
            tipFormatter={toShortIsoString}
            tooltipPlacement='bottom'
        />
    </DateRangeContainer>
}
