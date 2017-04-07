# lending-club-data-analysis

docker build  -t leanding-club .

docker run leanding-club  --module HandlingMissingValues  HandleMissingData  --local-scheduler

refer luigi_instructions.readme for local luigi commands


Summarization of lending dataset
Data-Analysis.ipynb
Summarization-Lending-Club-Data-Set.pdf



Reference for luigi 
https://github.com/pysysops/docker-luigi-taskrunner




Dervied Columns Links
revolving utilization

http://blog.credit.com/2013/04/what-is-revolving-utilization-65530/

Credit Age

https://www.nerdwallet.com/blog/finance/credit-age-length-of-credit-history/
earliest_cr_line and last_credit_pull_d date


Declined loans
Risk Score Nan--How to get estimate credit score

Grade
http://investorhelp.upstart.com/114489-what-do-the-loan-grades-mean

SubGrade plus grade

Reference Link:
http://www.magnifymoney.com/blog/personal-loans/lendingclub-review-borrowers-insiders-reveal578301843
