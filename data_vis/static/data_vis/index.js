import React from 'react'
import ReactDom from 'react-dom'

import { MyResponsiveLine } from './LineChart'


ReactDom.render(
    <div style={{
        position: 'absolute',
        top: '80px',
        right: '150px',
        bottom: '100px',
        left: '150px',
    }}>
        <MyResponsiveLine />
    </div>,
    document.getElementById('mount_point'),
)
