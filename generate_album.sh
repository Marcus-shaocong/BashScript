#!/bin/bash
set -x

echo "Creating album..."
mkdir -p thumbs

cat <<EOF1 > index.html
<html>
<head>
<style>
body
{
width:470px;
margin:auto;
border: 1px dashed grey:
padding: 10px;
}

img
{
	margin: 5px;
	border: 1px solid black;
}
</style>

</head>
<body>
<center><h1> #album title</h1></center>
<p>

EOF1

for img in *.jpg;
do 
	convert "$img" -resize "100px" "thumbs/$img"
	echo "<a href=\"$img\" ><img src=\"thumbs/$img\" title=\"$img\" /></a>" >> index.html
done

cat <<EOF2 >> index.html
</p>
</body>
</html>
EOF2

echo end of 

