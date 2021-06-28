# leetcode-qn-filter

- 爬取 LeetCode 題目資料，以動態網頁方式呈現過濾資料
- 過濾條件
  - PaidOnly: 是否為付費題目
  - Difficult: 題目難度
  - Likes: 題目讚數
  - Dislikes: 題目倒讚數
  - Acs: 總合格次數
  - Submits: 總提交次數
  - AcsRate: Ac的比率
  - Number: 顯示多少筆結果
- RefreshDB : 重新爬取資料並建立資料庫
- 前端 : jQuery, AJAX, Bootstrap
- 後端 : Flask, Sqlite+Sqlalchemy

![image](https://github.com/JerryTheUser/leetcode-qn-filter/blob/main/page.png)
