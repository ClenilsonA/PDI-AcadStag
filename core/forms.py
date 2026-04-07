from django import forms


class BaseTailwindForm(forms.ModelForm):
    input_classes = (
        "w-full rounded-lg border border-gray-300 px-3 py-2 "
        "focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
    )

    file_input_classes = (
        "block w-full text-sm text-gray-700 "
        "file:mr-4 file:py-2 file:px-4 "
        "file:rounded-lg file:border-0 "
        "file:text-sm file:font-semibold "
        "file:bg-blue-50 file:text-blue-700 "
        "hover:file:bg-blue-100"
    )

    textarea_classes = (
        "w-full rounded-lg border border-gray-300 px-3 py-2 "
        "focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
    )

    checkbox_classes = "h-4 w-4 text-blue-600 rounded"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            widget = field.widget
            existing_classes = widget.attrs.get("class", "")

            if isinstance(widget, forms.CheckboxInput):
                widget.attrs["class"] = f"{self.checkbox_classes} {existing_classes}".strip()
            elif isinstance(widget, forms.ClearableFileInput):
                widget.attrs["class"] = f"{self.file_input_classes} {existing_classes}".strip()
            elif isinstance(widget, forms.Textarea):
                widget.attrs["class"] = f"{self.textarea_classes} {existing_classes}".strip()
            else:
                widget.attrs["class"] = f"{self.input_classes} {existing_classes}".strip()