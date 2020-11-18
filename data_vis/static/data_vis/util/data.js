import Cookies from 'js-cookie'

import { toShortIsoString } from './date'


export async function fetchData(urls) {
    const responses = await Promise.all(urls.map(url => fetch(url)))
    const jsons = await Promise.all(
        responses.map(response => response.json())
    )
    return jsons
}


export async function getInitialData() {
    return await fetchData([
        `/data_vis/api/data/distributed/`,
        '/data_vis/api/tags/',
    ])
}

export async function updateChartData(dateRange, updateAppState) {
    const [start, end] = dateRange.map(toShortIsoString)
    const [json] = await fetchData([
        `/data_vis/api/data/distributed/?start=${start}&end=${end}`
    ])
    updateAppState([start, end], json)
}

export async function findPatterns(dateRange, finderConfigs, csrfToken=null) {
    const [start, end] = dateRange.map(toShortIsoString)
    const response = await fetch(
        `/data_vis/api/analytics/finders/?start=${start}&end=${end}`,
        {
            method: 'POST',
            mode: 'same-origin',
            headers: {
                'Content-Type': 'application/json; charset=UTF-8',
                'X-CSRFToken': csrfToken || Cookies.get('csrftoken'),
                'X-Requested-With': 'XMLHttpRequest',
            },
            body: JSON.stringify(finderConfigs),
        }
    )
    return await response.json()
}

/**
Associates the patterns with the corresponding points in the chart and returns
them in the structure expected by the chart.
This might not be trivial because the points are evenly distributed across one
day. So distributing the points in a pattern may not have the same resulting
distribution as the original points.
Therefore, we match the IDs to be able to draw lines through the associated
points of a pattern.
*/
export function associatedPatterns(patterns, chartData) {
    return (
        Object.entries(patterns)
        .map(([seriesId, seriesPatterns]) => {
            const series = chartData.find(({ id }) => id === seriesId).data
            // O(1) lookup because there may be multiple patterns and we don't want
            // to reiterate all the data points each time.
            const pointsById = Object.fromEntries(
                series.map(point => [point.id, point])
            )
            const patternSeries = seriesPatterns.map(
                pattern => pattern.map(({ id }) => {
                    const associatedPoint = pointsById[id]
                    // Deep copy because the only nested property is 'tags'.
                    return {
                        ...associatedPoint,
                        tags: associatedPoint.tags.slice(0),
                    }
                })
            )
            return patternSeries.map((data, index) => ({
                id: `${seriesId} (Pattern #${index + 1})`,
                data,
            }))
        })
        .flat(1)
    )
}
