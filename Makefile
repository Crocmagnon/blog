update-themes:
	git submodule update --recursive --remote

new-post:
	hugo new posts/$(title)/index.md
