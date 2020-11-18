import Cookies from 'js-cookie'
import React, { useState, useCallback, useContext } from 'react'

// import { getCsrfContext } from './context/csrf'
import { findPatterns } from './util/data'


const identity = x => x


const PatternFinder = props => {
    const {
        index,
        update: updateFinder,
        remove: removeFinder,
        fields,
        config,
    } = props

    // const update = useCallback(
    //     // (key, value) => updateFinder({index, config}),
    //     (key, value) => updateFinder({index, config}),
    //     [index, config, updateFinder],
    // )
    const remove = useCallback(
        () => removeFinder({index}),
        [index, removeFinder],
    )

    return <div>
        {fields.map(
            ([name, {label, component: Component, parseValue=identity, serializeValue=identity}]) => (
                <React.Fragment key={name}>
                    {label}:
                    <Component
                        value={serializeValue(config[name])}
                        // onChange={update}
                        onChange={useCallback(
                            (event) => {
                                // console.log('updating', name, 'at', index, 'to', parseValue(event.target.value))
                                updateFinder(
                                    index,
                                    {[name]: parseValue(event.target.value)},
                                )
                            },
                            // (event) => updateFinder(
                            //     index,
                            //     {[name]: parseValue(event.target.value)},
                            // ),
                            [updateFinder, name, index],
                        )}
                    />
                    <br />
                </React.Fragment>
            )
        )}
        <button onClick={remove}>-</button>
    </div>
}


const FREQUENCY_PATTERN_FINDER_FIELDS = [
    ['min_length', {
        label: 'Min. length',
        component: props => <input type='number' step='1' min='1' {...props} />,
        parseValue: value => Number.parseInt(value, 10) || 0,
    }],
    ['precision', {
        label: 'Precision',
        component: props => <select {...props}>
            <option value='days'>days</option>
        </select>,
    }],
    ['intervals', {
        label: 'Intervals',
        component: props => <input {...props} />,
        parseValue: value => {
            try {
                return JSON.parse(value)
            }
            catch (error) {
                return value
            }
        },
        serializeValue: value => (
            typeof value === 'string' || value instanceof String
            ? value
            : JSON.stringify(value)
        )
    }],
    ['tolerance_y', {
        label: 'Y tolerance',
        component: props => <input type='number' step='1' {...props} />,
        parseValue: value => Number.parseInt(value, 10) || 0,
    }],
]

const FrequencyPatternFinder = props => <PatternFinder
    // fields={FREQUENCY_PATTERN_FINDER_FIELDS}
    {...props}
/>
FrequencyPatternFinder.defaultProps = {
    config: {
        min_length: 2,
        precision: 'days',
        intervals: [{months: 1}],
        tolerance_y: 0,
    },
    fields: FREQUENCY_PATTERN_FINDER_FIELDS,
}


// const CsrfTokenContext = getCsrfContext()

export const PatternFinders = ({ dateRange, applyPatterns }) => {
    // const csrf = useContext(CsrfTokenContext)
    const [finders, setFinders] = useState([])
    const updateFinder = useCallback(
        (updateIndex, updateConfig) => setFinders(
            finders.map((config, index) => (
                index === updateIndex
                ? {...config, ...updateConfig}
                : config
            ))
        ),
        [finders, setFinders],
    )
    const addFinder = useCallback(
        () => setFinders([
            ...finders,
            {...FrequencyPatternFinder.defaultProps.config},
        ]),
        [finders, setFinders],
    )
    const removeFinder = useCallback(
        ({index}) => setFinders(finders.filter((_, i) => i !== index)),
        [finders, setFinders],
    )
    const submit = useCallback(
        async () => {
            applyPatterns(await findPatterns(dateRange, finders))
        },
        [finders],
    )

    return <>
        {
            finders.map(
                (finder, index) => <FrequencyPatternFinder
                    key={index}
                    index={index}
                    update={updateFinder}
                    remove={removeFinder}
                    config={finder}
                />
            )
        }
        {/* <FrequencyPatternFinder placeholder={true} /> */}
        <button onClick={addFinder}>+</button>
        <button>auto</button>
        <button
            type='submit'
            onClick={submit}
            disabled={finders.length === 0}
        >
            Submit
        </button>
    </>
}
