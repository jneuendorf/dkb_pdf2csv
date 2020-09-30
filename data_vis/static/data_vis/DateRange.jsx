import React, { useState, useEffect } from 'react'
import { createSliderWithTooltip, Range } from 'rc-slider'
import styled from 'styled-components'

import { updateChartData } from './util/data'
import { toShortIsoString } from './util/date'


const TooltipRange = createSliderWithTooltip(Range)


const DateRangeContainer = styled.div`
    padding: 10px 50px;
`


export const DateRange = ({min, max, setChartData}) => {
    const [dateRange, setDateRange] = useState([min, max])

    return <DateRangeContainer>
        <TooltipRange
            min={min}
            max={max}
            value={dateRange}
            onChange={setDateRange}
            onAfterChange={range => updateChartData(range, setChartData)}
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
