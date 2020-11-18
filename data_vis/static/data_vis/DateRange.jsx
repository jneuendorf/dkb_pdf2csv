import React, { useState, useCallback } from 'react'
import { createSliderWithTooltip, Range } from 'rc-slider'
import styled from 'styled-components'

import { updateChartData } from './util/data'
import { toShortIsoString } from './util/date'


const TooltipRange = createSliderWithTooltip(Range)


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

    return <DateRangeContainer>
        <button onClick={decreaseMin}>&lt;</button>
        <TooltipRange
            min={min}
            max={max}
            value={dateRange}
            onChange={setDateRange}
            onAfterChange={range => updateChartData(range, updateAppState)}
            step={24 * 60 * 60 * 1000}
            allowCross={false}
            pushable={true}
            tipFormatter={toShortIsoString}
            tipProps={{
                placement: 'bottom',
            }}
        />
    </DateRangeContainer>
}
