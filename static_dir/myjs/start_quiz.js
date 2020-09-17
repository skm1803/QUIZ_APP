  $( document ).ready(function() {
    console.log( "ready!" );
    $('.alert').hide(); 
});
  
  function checkAnswer(){
    console.log("clicked btn");
    let question_number = "{{next_question|add:"-2"}}"
    console.log(question_number);
    let answer_chosen = $("input[name='answer-option']:checked").val();

    if (answer_chosen === undefined){
       document.getElementById("alert-msg").innerHTML +=
       `<div class="alert alert-warning alert-dismissible fade show" role="alert">
        Please select an option.
        <button type="button" class="close" data-dismiss="alert" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>`
    }
    if (answer_chosen !== undefined)
      checkIfCorrect(question_number,answer_chosen);
  }


 function checkIfCorrect(question_number,answer_chosen){

    console.log("here ques",question_number);
    chosen_answer_id = $("input[name='answer-option']:checked").attr('id');
    console.log(chosen_answer_id);
    var token = "{{csrf_token}}";
    $.ajax({
            type: "POST",
            headers: { "X-CSRFToken": token },
            url: "/check-correct/{{quiz_object.slug}}/" + question_number +"/",
            data: { 'answer_chosen':answer_chosen,'chosen_answer_id':chosen_answer_id },

            success: function (data) {

              console.log(data);
              let wrongSpan = $(`#${data.chosen_answer}`);
              console.log(wrongSpan)
              wrongSpan.addClass('wrong');
              let rightSpan = $(`#${data.right_answer}`);
              console.log(rightSpan)
              rightSpan.addClass('right-ans');

              },
            error: function (data) {
              console.log("error");
            },
          });
 }
