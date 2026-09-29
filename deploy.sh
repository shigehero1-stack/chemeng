#!/bin/sh
# サイトを生成して gh-pages ブランチに公開する（GitHub Pages）
set -e
cd "$(dirname "$0")"
python3 build.py
touch public/.nojekyll
TMP=$(mktemp -d)
cp -R public/. "$TMP"
cd "$TMP"
git init -q -b gh-pages
git add -A
git -c user.name="$(git -C "$OLDPWD" config user.name)" -c user.email="$(git -C "$OLDPWD" config user.email || echo noreply@example.com)" commit -q -m "Deploy $(date '+%Y-%m-%d %H:%M')"
git push -q -f "$(git -C "$OLDPWD" remote get-url origin)" gh-pages
cd - >/dev/null
rm -rf "$TMP"
echo "公開しました: https://chemeng-nyumon.com/"
