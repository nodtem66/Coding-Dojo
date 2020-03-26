# Coding Dojo
[![Build Status](https://dev.azure.com/n66/PublicCI/_apis/build/status/nodtem66.Coding-Dojo?branchName=master)](https://dev.azure.com/n66/PublicCI/_build/latest?definitionId=3&branchName=master)
> https://github.com/saladpuk/Coding-Dojo

## โปรแกรมตัดเกรด
ตัวโปรแกรมจะให้กรอกคะแนน 0~100 ลงไป แล้วบอกว่าได้เกรดอะไร

### เกณฑ์การให้เกรด
|เกรด|ช่วงคะแนน|
|--|--|
|A|91~100|
|B|81~90|
|C|71~80|
|D|61~70|
|F|0~60|

### Requirements
1. **Python** 3.5

## Design concept
1. คิดเผื่อการแก้เกณฑ์การตัดเกรดซึ่งผู้ใช้แต่ละคนจะมีแนวคิดที่ต่างกันไป
2. `Grader > SakulGrader` เป็นการตัดเกรดจากเกณฑ์ @sakul ตัวอย่างการใช้งานใน `simple.py`
3. `SakulGrader > ExtendedSakulGrade` เป็นการเพิ่มเติมเกณฑ์ ในกรณีคะแนนเป็นทศนิยมจะทำการปัดเศษ .5 ขึ้น คะแนนที่อยู่นอกช่วงจะได้ X
4. `Grader > ConfigGrader` เพิ่มเติมการโหลด config file
5. `Grader > ConfigGrader > JsonGrader` ตัดเกรดจากเกณฑ์ในไฟล์ JSON ตัวอย่างการใช้งานใน `main.py`
6. `test.py` ใช้ _unittest_ ทดสอบ Grader ต่างๆ

## Simple usage
- `python simple.py`

## ตัวอย่าง Configuration ใน JsonGrader
```json
{
    "round": 0,
    "criterias": [
        { "from": 0, "to": 49, "grade": "F"},
        { "from": 50, "to": 54, "grade": "D"},
        { "from": 55, "to": 59, "grade": "D+"},
        { "from": 60, "to": 64, "grade": "C"},
        { "from": 65, "to": 69, "grade": "C+"},
        { "from": 70, "to": 74, "grade": "B"},
        { "from": 75, "to": 79, "grade": "B+"},
        { "from": 80, "to": 100, "grade": "A"},
        { "from": 100, "grade": "A+"}
    ],
    "default": "-"
}
```

## Running
- `python main.py 59`
- `python main.py 59 60 70 80 90 100 -g Sakul`
- `python main.py 59 60 70 80 90 100 -c grader_config_example.json`

## Testing
`python test.py`