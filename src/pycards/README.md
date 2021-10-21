# pycards: card game Python utilities

Features:

  * Combine card images to PDF.
  * Example how to download CSV data from Google sheets.
  * Rendering (biggest part).

## Rendering examples

One interesting function is:

    render_text_with_assets(
      rxy, 
      text, 
      img, 
      font, 
      text_color, 
      assets, 
      align,
      max_width
    )

Which prints to image `img` the `text` in location `rxy`.
The `text` can contain asset images, for example:
`"print a rabbit: {rabbit}"`, where `{rabbit}` is a reference
to a rabbit image in the `assets` dictionary
`{"rabbit": <img>, ...}`.
