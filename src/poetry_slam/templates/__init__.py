from .project_template import ProjectTemplate, TEMPLATE_ROOT


def templates():
    avail = dict()
    for p in TEMPLATE_ROOT.iterdir():
        if p.is_dir():
            avail[p.name] = ProjectTemplate(p)
    return avail
