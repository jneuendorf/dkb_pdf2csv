import React, { useCallback } from 'react'
import {
    Spin,
    Form,
    Checkbox,
} from 'antd'
import styled from 'styled-components'


const FormWrapper = styled.div`min-height: 100px;`


export const TagFilter = ({tags, highlightedTags, setHighlightedTags}) => {
    const toggleCheckbox = useCallback(
        event => {
            const {
                target: {
                    checked,
                    "data-tag": tag,
                },
            } = event
            if (checked) {
                setHighlightedTags([...highlightedTags, tag])
            }
            else {
                setHighlightedTags(highlightedTags.filter(
                    ignoredTag => ignoredTag !== tag
                ))
            }
        },
        [highlightedTags, setHighlightedTags],
    )

    return <Spin
        spinning={tags.length === 0}
        tip='Loading...'
        delay={100}
    >
        <FormWrapper>
            <Form layout='vertical' size='small'>
                {
                    tags
                    .filter(({is_abstract}) => !is_abstract)
                    .map(({identifier: tag}) => {
                        const checked = highlightedTags.indexOf(tag) >= 0
                        return <Form.Item key={tag}>
                            <Checkbox
                                data-tag={tag}
                                checked={checked}
                                onChange={toggleCheckbox}
                            >
                                {tag}
                            </Checkbox>
                        </Form.Item>
                    })
                }
            </Form>
        </FormWrapper>
    </Spin>

}
