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
        // fetch(`/data_vis/data/${search}&start=null&end=null`),
        `/data_vis/data/distributed/`,
        // fetch(`/data_vis/data_raw/`),
        '/data_vis/tags/',
    ])
}

export async function updateChartData(dateRange, setChartData) {
    const [start, end] = dateRange
    const [json] = await fetchData([
        `/data_vis/data/distributed/?start=${toShortIsoString(start)}&end=${toShortIsoString(end)}`
    ])
    setChartData(json)
}
