# Beide (jhead & find) nog niet gestest, maar zou moeten werken volgen claude
shopt -s globstar nullglob nocaseglob
jhead -autorot **/*.{jpg,jpeg,JPG,JPEG}
find . -type f \( -iname "*.jpg" -o -iname "*.jpeg" \) -exec jhead -autorot {} +
