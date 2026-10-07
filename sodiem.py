from flask import (
    Flask, url_for, request, redirect,
    abort, make_response, jsonify
)
from markupsafe import escape

app = Flask(__name__)
app.json.ensure_ascii = False



STUDENTS = {
    "23T1020001": {
        "name": "Nguyễn Văn An",
        "lop": "K47A",
        "scores": {"PMMNM": 8.5, "CSDL": 7.0, "MMT": 9.0},
    },
    "23T1020002": {
        "name": "Trần Thị Bình",
        "lop": "K47A",
        "scores": {"PMMNM": 6.0, "CSDL": 5.5, "MMT": 7.0},
    },
    "23T1020003": {
        "name": "Lê Hoàng Cường",
        "lop": "K47B",
        "scores": {"PMMNM": 9.5, "CSDL": 9.0},
    },
    "23T1020004": {
        "name": "Phạm Minh Dũng",
        "lop": "K47B",
        "scores": {"PMMNM": 4.0, "CSDL": 3.5, "MMT": 5.0},
    },
    "23T1020005": {
        "name": "Hoàng Thu Hà",
        "lop": "K47A",
        "scores": {},
    },
    "23T1020006": {
        "name": "Võ Quốc Khánh",
        "lop": "K47C",
        "scores": {"PMMNM": 7.5, "MMT": 8.0},
    },
}




def average(scores):
    if not scores:
        return None

    return round(sum(scores.values()) / len(scores), 2)


def rank(avg):
    if avg is None:
        return "Chưa có điểm"

    if avg >= 8.5:
        return "Giỏi"

    if avg >= 7.0:
        return "Khá"

    if avg >= 5.0:
        return "Trung bình"

    return "Yếu"


def student_summary(mssv):
    student = STUDENTS[mssv]

    avg = average(student["scores"])

    return {
        "mssv": mssv,
        "name": student["name"],
        "lop": student["lop"],
        "scores": student["scores"],
        "average": avg,
        "rank": rank(avg),
    }


def layout(title, body):
    return f"""
    <!DOCTYPE html>

    <html lang="vi">

    <head>
        <meta charset="UTF-8">
        <title>{escape(title)} - Sổ điểm</title>
    </head>

    <body>

        <nav>
            <a href="{url_for('home')}">Trang chủ</a> |
            <a href="{url_for('student_list')}">Sinh viên</a> |
            <a href="{url_for('search')}">Tìm kiếm sinh viên</a>
        </nav>

        <hr>

        <h1>{escape(title)}</h1>

        {body}

    </body>

    </html>
    """



# C1

@app.route("/")
def home():

    total_students = len(STUDENTS)

    classes = set(
        student["lop"]
        for student in STUDENTS.values()
    )

    body = f"""
        <p>
            Tổng số sinh viên:
            <strong>{total_students}</strong>
        </p>

        <p>
            Số lớp:
            <strong>{len(classes)}</strong>
        </p>

        <p>
            <a href="{url_for('student_list')}">
                Danh sách sinh viên
            </a>
        </p>

        <p>
            <a href="{url_for('api_students')}">
                API sinh viên
            </a>
        </p>
    """

    return layout("Trang chủ", body)


# C2

@app.route("/students")
def student_list():

    lop = request.args.get("lop", "").strip()

    classes = sorted({
        student["lop"]
        for student in STUDENTS.values()
    })

    body = f"""
        <p>
            <a href="{url_for('student_list')}">
                Tất cả
            </a>
    """

    for class_name in classes:

        body += f"""
            |
            <a href="{url_for('student_list', lop=class_name)}">
                {escape(class_name)}
            </a>
        """

    body += "</p>"

    students = []

    for mssv in STUDENTS:

        student = student_summary(mssv)

        if (
            not lop
            or student["lop"].lower() == lop.lower()
        ):
            students.append(student)

    if not students:

        body += "<p>Không có sinh viên phù hợp.</p>"

        return layout(
            "Danh sách sinh viên",
            body
        )

    body += """
        <table border="1" cellpadding="8">

        <tr>
            <th>MSSV</th>
            <th>Họ tên</th>
            <th>Lớp</th>
            <th>Điểm TB</th>
            <th>Xếp loại</th>
        </tr>
    """

    for student in students:

        avg = (
            "—"
            if student["average"] is None
            else student["average"]
        )

        body += f"""
        <tr>

            <td>
                <a href="{
                    url_for(
                        'student_detail',
                        mssv=student['mssv']
                    )
                }">
                    {escape(student['mssv'])}
                </a>
            </td>

            <td>
                {escape(student['name'])}
            </td>

            <td>
                {escape(student['lop'])}
            </td>

            <td>
                {escape(str(avg))}
            </td>

            <td>
                {escape(student['rank'])}
            </td>

        </tr>
        """

    body += "</table>"

    return layout(
        "Danh sách sinh viên",
        body
    )



# C3


@app.route("/students/<mssv>")
def student_detail(mssv):

    if mssv not in STUDENTS:

        abort(
            404,
            description=
            f"Không có sinh viên với MSSV = {mssv}."
        )

    student = student_summary(mssv)

    avg = (
        "—"
        if student["average"] is None
        else student["average"]
    )

    body = f"""
        <p>
            Họ tên:
            {escape(student['name'])}
        </p>

        <p>
            MSSV:
            {escape(student['mssv'])}
        </p>

        <p>
            Lớp:

            <a href="{
                url_for(
                    'student_list',
                    lop=student['lop']
                )
            }">
                {escape(student['lop'])}
            </a>
        </p>

        <p>
            Điểm TB:
            {escape(str(avg))}
        </p>

        <p>
            Xếp loại:
            {escape(student['rank'])}
        </p>

        <h2>Bảng điểm</h2>
    """

    if student["scores"]:

        body += """
            <table border="1" cellpadding="8">

            <tr>
                <th>Học phần</th>
                <th>Điểm</th>
            </tr>
        """

        for course, score in student["scores"].items():

            body += f"""
            <tr>
                <td>{escape(course)}</td>
                <td>{escape(str(score))}</td>
            </tr>
            """

        body += "</table>"

    else:

        body += "<p>Chưa có điểm.</p>"

    body += f"""
        <p>
            <a href="{
                url_for(
                    'export_scores',
                    mssv=mssv
                )
            }">
                Tải bảng điểm (CSV)
            </a>
        </p>

        <p>
            Link rút gọn:
            <a href="{
                url_for(
                    'short_student',
                    mssv=mssv
                )
            }">
                {escape(
                    url_for(
                        'short_student',
                        mssv=mssv
                    )
                )}
            </a>
        </p>
    """

    return layout(
        "Chi tiết sinh viên",
        body
    )



# C4

@app.route("/sv/<mssv>")
def short_student(mssv):

    return redirect(
        url_for(
            "student_detail",
            mssv=mssv
        ),
        code=301
    )



# C5


@app.route("/students/<mssv>/export")
def export_scores(mssv):

    if mssv not in STUDENTS:

        abort(
            404,
            description=
            f"Không có sinh viên với MSSV = {mssv}."
        )

    lines = ["hoc_phan,diem"]

    for course, score in (
        STUDENTS[mssv]["scores"].items()
    ):

        lines.append(
            f"{course},{score}"
        )

    csv_content = "\n".join(lines)

    response = make_response(csv_content)

    response.headers["Content-Type"] = (
        "text/csv; charset=utf-8"
    )

    response.headers[
        "Content-Disposition"
    ] = (
        f"attachment; "
        f"filename=diem_{mssv}.csv"
    )

    return response



# C6

@app.route("/search")
def search():

    q = request.args.get(
        "q",
        ""
    ).strip()

    safe_q = escape(q)

    body = f"""
        <form method="GET"
              action="{url_for('search')}">

            <input
                type="text"
                name="q"
                value="{safe_q}"
            >

            <button type="submit">
                Tìm kiếm
            </button>

        </form>
    """

    if q:

        results = []

        for mssv, student in (
            STUDENTS.items()
        ):

            if (
                q.lower()
                in student["name"].lower()
                or q.lower()
                in mssv.lower()
            ):

                results.append(
                    (mssv, student)
                )

        body += f"""
            <p>
                Tìm thấy
                {len(results)}
                kết quả cho
                "{safe_q}"
            </p>
        """

        body += "<ul>"

        for mssv, student in results:

            body += f"""
                <li>

                    <a href="{
                        url_for(
                            'student_detail',
                            mssv=mssv
                        )
                    }">

                        {escape(mssv)}
                        -
                        {escape(student['name'])}

                    </a>

                </li>
            """

        body += "</ul>"

    return layout(
        "Tìm kiếm sinh viên",
        body
    )


# C7 

@app.route("/api/students")
def api_students():

    lop = request.args.get(
        "lop",
        ""
    ).strip()

    raw_min_avg = request.args.get(
        "min_avg"
    )

    min_avg = None

    if raw_min_avg is not None:

        try:
            min_avg = float(
                raw_min_avg
            )

        except ValueError:

            abort(
                400,
                description=
                "min_avg phải là một số."
            )

    results = []

    for mssv in STUDENTS:

        student = student_summary(
            mssv
        )

        if (
            lop
            and student["lop"].lower()
            != lop.lower()
        ):
            continue

        if min_avg is not None:

            if student["average"] is None:
                continue

            if (
                student["average"]
                < min_avg
            ):
                continue

        results.append(student)

    return jsonify(results)


@app.route("/api/students/<mssv>")
def api_student_detail(mssv):

    if mssv not in STUDENTS:

        abort(
            404,
            description=
            f"Không có sinh viên với MSSV = {mssv}."
        )

    return jsonify(
        student_summary(mssv)
    )


# C8

@app.route(
    "/api/students/<mssv>/scores/<course>",
    methods=["GET", "PUT", "DELETE"]
)
def manage_score(mssv, course):

    if mssv not in STUDENTS:

        abort(
            404,
            description=
            f"Không có sinh viên với MSSV = {mssv}."
        )

    course = course.upper()

    scores = STUDENTS[mssv]["scores"]

    if request.method == "GET":

        if course not in scores:

            abort(
                404,
                description=
                f"Chưa có điểm học phần {course}."
            )

        return jsonify({
            "mssv": mssv,
            "course": course,
            "score": scores[course]
        })

    if request.method == "PUT":

        raw_score = request.args.get(
            "score"
        )

        if raw_score is None:

            abort(
                400,
                description=
                "Thiếu tham số score."
            )

        try:
            score = float(raw_score)

        except ValueError:

            abort(
                400,
                description=
                "score phải là một số."
            )

        if score < 0 or score > 10:

            abort(
                400,
                description=
                "Điểm phải nằm trong khoảng từ 0 đến 10."
            )

        existed = course in scores

        scores[course] = score

        data = {
            "mssv": mssv,
            "course": course,
            "score": score,
            "average": average(scores)
        }

        if existed:

            return jsonify(data), 200

        response = make_response(
            jsonify(data),
            201
        )

        response.headers["Location"] = (
            url_for(
                "manage_score",
                mssv=mssv,
                course=course
            )
        )

        return response


    if course not in scores:

        abort(
            404,
            description=
            f"Chưa có điểm học phần {course}."
        )

    del scores[course]

    return "", 204


# C9

@app.errorhandler(400)
@app.errorhandler(404)
@app.errorhandler(405)
def handle_error(error):

    titles = {
        400: "Dữ liệu không hợp lệ",
        404: "Không tìm thấy",
        405: "Phương thức không được hỗ trợ"
    }

    title = titles.get(
        error.code,
        "Lỗi"
    )

    if request.path.startswith(
        "/api/"
    ):

        return jsonify({
            "error": title,
            "detail": error.description
        }), error.code

    body = f"""
        <p>
            Mã lỗi:
            {escape(str(error.code))}
        </p>

        <p>
            {escape(error.description)}
        </p>
    """

    return layout(
        title,
        body
    ), error.code




if __name__ == "__main__":
    app.run(debug=True)