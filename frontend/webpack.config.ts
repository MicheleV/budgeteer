import path from "path";
import webpack from "webpack";
import ForkTsCheckerWebpackPlugin from 'fork-ts-checker-webpack-plugin'; // TODO: do we need this?
const FileManagerPlugin = require('filemanager-webpack-plugin');

const config: webpack.Configuration = {
  entry: "./src/index.tsx",
  module: {
    rules: [
      {
        test: /\.(ts|js)x?$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader",
          options: {
            presets: [
              "@babel/preset-env",
              "@babel/preset-react",
              "@babel/preset-typescript",
            ],
          },
        },
      },
    ],
  },
  resolve: {
    extensions: [".tsx", ".ts", ".js"],
  },
  output: {
    path: path.resolve(__dirname, "build"),
    filename: "bundle.js",
  },
  devServer: {
    contentBase: path.join(__dirname, "build"),
    compress: true,
    port: 4000,
  },
  // TODO: add logic to control this in dev/prod
  optimization: {
    minimize: false
  },
  plugins: [
    new FileManagerPlugin({
      events: {
        onEnd: {
          delete: ['/bundle.js', '../app/budgets/static/js/bundle.js'],
          copy: [
            {source: 'build/bundle.js', destination: '../app/budgets/static/js/bundle.js', force: true},
            {source: 'build/bundle.js', destination: '../app/static/js/bundle.js', force: true}, // TODO: this is not strictly needed: we should run "python manage.py collectstatic" instead
          ],
      },
      }
    }),
  ],
};

export default config;