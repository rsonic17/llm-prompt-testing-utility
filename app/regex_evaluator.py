
import traceback
import re

def safely_execute_regex_function(code_str: str, text: str):
    """
    Executes LLM-generated regex code safely and returns normalized output.
    Supports nested fields like list of invoices.
    """
    local_env = {}

    try:
        exec(code_str, {}, local_env)

        if 'extract_fields' not in local_env:
            return {}, "extract_fields function not defined in regex code."

        raw_result = local_env['extract_fields'](text)
        cleaned = {}

        for key, val in raw_result.items():
            if isinstance(val, re.Match):
                try:
                    cleaned[key] = val.group(1).strip()
                except Exception:
                    cleaned[key] = ""
            elif isinstance(val, list):
                cleaned_list = []
                for item in val:
                    if isinstance(item, dict):
                        sub = {}
                        for k, v in item.items():
                            if isinstance(v, re.Match):
                                try:
                                    sub[k] = v.group(1).strip()
                                except Exception:
                                    sub[k] = ""
                            else:
                                sub[k] = str(v).strip()
                        cleaned_list.append(sub)
                    else:
                        cleaned_list.append(str(item).strip())
                cleaned[key] = cleaned_list
            elif val is None:
                cleaned[key] = ""
            else:
                cleaned[key] = str(val).strip()

        return cleaned, None

    except Exception as e:
        return {}, f"Regex error: {e}\n{traceback.format_exc()}"
