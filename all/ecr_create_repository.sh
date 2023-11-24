#!/bin/bash

current_dir_name=$(basename "$(pwd)")

# リポジトリ名を設定
REPOSITORY_NAME="$current_dir_name"

# AWS リージョンを設定（必要に応じて変更してください）
AWS_REGION="ap-northeast-1"

echo "REPOSITORY_NAME: ${REPOSITORY_NAME}"
echo "AWS_REGION: ${AWS_REGION}"

confirm() {
  echo -n "$1 (yes/no): "
  read answer
  case "$answer" in
    yes|Yes|YES) return 0 ;;
    *) return 1 ;;
  esac
}

if confirm "リポジトリ '${REPOSITORY_NAME}' を作成してもよろしいですか？"; then
  # Amazon ECR リポジトリを作成
  result=$(aws ecr create-repository --repository-name "${REPOSITORY_NAME}" --region "${AWS_REGION}" 2>&1)
  if [ $? -eq 0 ]; then
    echo "リポジトリの作成が完了しました。"
  else
    echo "エラー: リポジトリの作成に失敗しました。"
    echo "$result"
    exit 1
  fi
else
  echo "キャンセルされました。"
fi
