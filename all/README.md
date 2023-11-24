# instagram api list
## - get-account-data-instagram-test

## 概要
本プロジェクトは、Instagram APIを利用して特定のInstagramアカウントからデータを取得し、そのデータをスプレッドシートに入力する自動化システムです。AWSのEvent Bridgeを使用して、この処理を毎日1回自動で実行します。

## Instagram基本表示API
Instagram基本表示APIは、Instagramユーザーのプロファイル情報、写真、ビデオなどのコンテンツを取得するためのAPIです。このAPIは主に個人用アカウントに焦点を当てており、アプリケーションがInstagramユーザーの代わりにInstagramの基本的な情報を取得するために使用されます。

- 詳細: [Instagram基本表示APIドキュメント](https://developers.facebook.com/docs/instagram-basic-display-api)

## InstagramグラフAPI
InstagramグラフAPIは、ビジネスアカウントやクリエイターアカウントのためのAPIです。このAPIを使用することで、ビジネスアカウントやクリエイターアカウントの解析データ、メディアオブジェクトの管理、コメントのモデレーションなどの機能にアクセスすることができます。

- 詳細: [InstagramグラフAPIドキュメント](https://developers.facebook.com/docs/instagram-api)


## CI/CDの構成
CI/CDプロセスは、GitHub ActionsとAWS CloudFormationを組み合わせて構成されます。このワークフローにより、コードの変更が自動的にデプロイされ、プロジェクトの継続的な統合とデリバリーが実現されます。

## 使用方法

### リポジトリの作成
1. プロジェクトディレクトリに移動します。
2. `./ecr_create_repository` スクリプトを実行して、Amazon ECRのリポジトリを作成します。

    ```bash
    ./ecr_create_repository
    ```

### GitHubでのプッシュ
1. mainブランチに変更をコミットします。この際、コミットメッセージに `<project名 or directory名 or repository名>` を含めると、そのディレクトリを対象にデプロイが行われます。
2. 変更をGitHubのmainブランチにプッシュします。

    ```bash
    git commit -m "<project名 or directory名 or repository名> commit message"
    ```
    ```bash
    git push origin main
    ```