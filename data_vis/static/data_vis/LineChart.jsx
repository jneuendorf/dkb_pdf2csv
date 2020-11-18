import React, { useState, useCallback } from 'react'
import Switch from 'rc-switch'
import { ResponsiveLine } from '@nivo/line'
import styled from 'styled-components'

import { DotsItemSymbol } from './DotsItemSymbol'
import { ToolTip } from './ToolTip'


const SwitchContainer = styled.div`
    margin: 30px 0 0 50px;
`


export const LineChart = ({ data, highlightedTags, onClick }) => {
    const [ignoredSeries, setIgnoredSeries] = useState([])
    const [yAttribute, setYAttribute] = useState('y')

    const regardedSeries = data.map(series => {
        if (ignoredSeries.indexOf(series.id) >= 0) {
            return {...series, data: []}
        }
        else {
            return {
                ...series,
                data: series.data.map(point => ({
                    ...point,
                    y: point[yAttribute],
                }))
            }
        }
    })

    const toggleYAttribute = useCallback(
        (checked, event) => setYAttribute(checked ? 'dy' : 'y'),
        [setYAttribute],
    )

    return <React.Fragment>
        <SwitchContainer>
            {'y '}
            <Switch onChange={toggleYAttribute} />
            {' dy'}
        </SwitchContainer>
        <ResponsiveLine
            data={regardedSeries}
            margin={{ top: 50, right: 110, bottom: 50, left: 60 }}
            xScale={{
                type: 'time',
                // https://github.com/d3/d3-time-format#isoParse
                format: '%Y-%m-%dT%H:%M:%S%Z',
                useUTC: true,
                // useUTC: false,
                // precision: 'day',
                // precision: 'millisecond',
                precision: 'minute',
            }}
            yScale={{
                type: 'linear',
                min: 'auto',
                max: 'auto',
                stacked: false,
                reverse: false,
            }}
            axisTop={null}
            axisRight={null}
            axisBottom={{
                orient: 'bottom',
                tickSize: 5,
                tickPadding: 5,
                tickRotation: 0,
                format: '%b %d',
                tickValues: 'every month',
                legend: 'Date',
                legendOffset: 36,
                legendPosition: 'middle'
            }}
            axisLeft={{
                orient: 'left',
                tickSize: 5,
                tickPadding: 5,
                tickRotation: 0,
                legend: 'EUR',
                legendOffset: -40,
                legendPosition: 'middle'
            }}
            colors={{ scheme: 'nivo' }}
            pointSize={5}
            pointColor={{ theme: 'background' }}
            pointBorderWidth={1.8}
            pointBorderColor={{ from: 'serieColor' }}
            pointLabel="y"
            pointLabelYOffset={-12}
            // TODO: Don't recreate component every time
            pointSymbol={props => <DotsItemSymbol
                {...props}
                highlightedTags={highlightedTags}
            />}
            useMesh={true}
            legends={[
                {
                    anchor: 'bottom-right',
                    direction: 'column',
                    justify: false,
                    translateX: 100,
                    translateY: 0,
                    itemsSpacing: 0,
                    itemDirection: 'left-to-right',
                    itemWidth: 80,
                    itemHeight: 20,
                    itemOpacity: 0.75,
                    symbolSize: 12,
                    symbolShape: 'circle',
                    symbolBorderColor: 'rgba(0, 0, 0, .5)',
                    effects: [
                        {
                            on: 'hover',
                            style: {
                                itemBackground: 'rgba(0, 0, 0, .03)',
                                itemOpacity: 1
                            }
                        }
                    ],
                    onClick: (series, event) => {
                        if (ignoredSeries.indexOf(series.id) >= 0) {
                            setIgnoredSeries(ignoredSeries.filter(
                                ignoredId => ignoredId !== series.id
                            ))
                        }
                        else {
                            setIgnoredSeries([...ignoredSeries, series.id])
                        }
                    }
                }
            ]}
            tooltip={ToolTip}
            onClick={onClick}
        />
    </React.Fragment>
}
