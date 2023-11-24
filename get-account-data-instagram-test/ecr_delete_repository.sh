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

if confirm "リポジトリ '${REPOSITORY_NAME}' を削除してもよろしいですか？"; then
  # Amazon ECR リポジトリを削除
  result=$(aws ecr delete-repository --repository-name "${REPOSITORY_NAME}" --region "${AWS_REGION}" --force 2>&1)
  if [ $? -eq 0 ]; then
    echo "リポジトリの削除が完了しました。"
  else
    echo "エラー: リポジトリの削除に失敗しました。"
    echo "$result"
    exit 1
  fi
else
  echo "キャンセルされました。"
fi
