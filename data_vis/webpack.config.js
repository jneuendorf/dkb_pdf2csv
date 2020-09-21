module.exports = {
    mode: 'development',
    entry: {
        main: './static/data_vis/index.js',
    },
    output: {
        filename: '[name].js',
        path: __dirname + '/static/data_vis/dist',
    },
    module: {
        rules: [{
            test: /\.m?js$/,
            exclude: /node_modules/,
            use: {
                loader: "babel-loader",
                options: {
                    presets: ['@babel/preset-env']
                }
            }
        }]
    }
}
