import React from 'react'


export const TagFilter = ({tags, ignoredTags, setIgnoredTags}) => {
    return <ul>
        {
            tags
            .filter(({is_abstract}) => !is_abstract)
            .map(({identifier: tag}) => {
                const checked = ignoredTags.indexOf(tag) >= 0
                return <li key={tag}>
                    <input
                        type='checkbox'
                        checked={checked}
                        onChange={event => {
                            if (checked) {
                                setIgnoredTags(
                                    ignoredTags.filter(
                                        ignoredTag => ignoredTag !== tag
                                    )
                                )
                            }
                            else {
                                setIgnoredTags([...ignoredTags, tag])
                            }
                        }}
                    />
                    {tag}
                </li>
            })
        }
    </ul>
}
