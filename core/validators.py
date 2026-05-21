from django import forms


def validate_pdf_file(uploaded_file):
    if not uploaded_file:
        return uploaded_file

    if not uploaded_file.name.lower().endswith(".pdf"):
        raise forms.ValidationError("O ficheiro deve estar em formato PDF.")

    content_type = getattr(uploaded_file, "content_type", "")
    if content_type and content_type != "application/pdf":
        raise forms.ValidationError("O ficheiro deve ser um PDF válido.")

    return uploaded_file