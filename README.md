# Subjective-answer-checking
This is our project for Information Retieval course Offered in winter Semester 2020 at IIITD.  

Traditional answer evaluation, i.e., manual checking of answers takes a lot of time and energy. However, objective-type questions can be evaluated using computers very efficiently, but there is no platform for checking the answers very precisely and efficiently when it comes to theoretical evaluation of answers. So invariably, there is a need for a checker to check the answers manually, which takes a lot of effort and time, and sometimes he/she has to provide the feedback, which would again take a lot of effort and analysis. Hence, we propose a system that evaluates the assessment copies automatically according to the rubric set by the checker for every type of question(subjective and objective) and also for multiple types of copies like pdf, scanned pdf. Our system would also give feedback over every question in a sheet generated for each student.  



Main technique used are:-
  • Page segmentation technique to separate the Image of answer and question on the page. 
  • Google vision API to read the handwriting in answer segmented part. Google vision Api has more efficiency than python OCR Tools. 
  • Word2vec for calculating the similarity distance between ideal and written answers.
