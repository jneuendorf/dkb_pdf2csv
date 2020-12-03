import React from 'react'
import { Spin } from 'antd'


export const TagFilter = ({tags, highlightedTags, setHighlightedTags}) => {
    return <Spin
        spinning={tags.length === 0}
        tip='Loading...'
        delay={100}
    >
        <ul style={{ paddingInlineStart: '15px', minHeight: '120px' }}>
            {
                tags
                .filter(({is_abstract}) => !is_abstract)
                .map(({identifier: tag}) => {
                    const checked = highlightedTags.indexOf(tag) >= 0
                    const id = `checkbox_${tag}`
                    return <li
                        key={tag}
                        style={{ listStyleType: 'none' }}
                    >
                        <input
                            id={id}
                            type='checkbox'
                            checked={checked}
                            onChange={event => {
                                if (checked) {
                                    setHighlightedTags(highlightedTags.filter(
                                        ignoredTag => ignoredTag !== tag
                                    ))
                                }
                                else {
                                    setHighlightedTags([...highlightedTags, tag])
                                }
                            }}
                        />
                        <label htmlFor={id}>
                            {tag}
                        </label>
                    </li>
                })
            }
        </ul>
    </Spin>

}
