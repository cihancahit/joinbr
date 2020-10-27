const path = require("path");
const webpack = require("webpack");
const MiniCssExtractPlugin = require('mini-css-extract-plugin')
//d

const config = {
    mode: "development",
    entry: "./client/src/index.js",
    output: {
        path: path.resolve(__dirname, "static/fec/js"), // string
        filename: "bundle.js",
        publicPath: "/static/"
    },
    module: {
        rules: [
            {
                test: /\.(gif|png|jpe?g|svg)$/i,
                use: [
                    'file-loader',
                    {
                        loader: 'image-webpack-loader',
                        options: {
                            bypassOnDebug: true, // webpack@1.x
                            disable: true, // webpack@2.x and newer
                        },
                    },
                ],
            },
            {
                test: /\.(js|jsx)$/,
                exclude: /node_modules/,
                use: {
                    loader: "babel-loader",
                    options: {
                        presets: ['@babel/react', '@babel/preset-env'],
                        plugins: ['@babel/proposal-class-properties']
                    }
                }
            },
            {
                test: /\.(scss|css)$/,
                use: [
                    {
                        loader: 'style-loader'
                    },
                    {
                        loader: 'css-loader'
                    },
                    {
                        loader: 'sass-loader'
                    }
                ]
            },
            {
                test: /\.(png|woff|woff2|eot|ttf|svg)$/,
                loader: 'url-loader?limit=100000'
            }
        ]
    },
    plugins: [
        new MiniCssExtractPlugin({
            filename: this.mode === "development" ? '[name].css' : '[name].[hash].css',
            chunkFilename: this.mode === "development" ? '[id].css' : '[id].[hash].css'
        })
    ]
}
module.exports = config;