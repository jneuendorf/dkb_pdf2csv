module.exports = {
    mode: 'development',
    entry: {
        main: './static/data_vis/main.js',
    },
    output: {
        filename: '[name].js',
        path: __dirname + '/static/data_vis/dist',
    },
    module: {
        rules: [{
            test: /\.jsx?$/,
            exclude: /node_modules/,
            use: {
                loader: "babel-loader",
            }
        }]
    },
    resolve: {
        extensions: ['.js', '.jsx'],
    },
    // devtool: 'inline-source-map',
    devtool: 'eval-cheap-module-source-map',
}
