$(document).ready(function(){


/*
--------------------------------------------------------
********************FOR SORTING*************************
--------------------------------------------------------
*/

$("#button-sort-employee").click(function(e){
    e.preventDefault();
    var column = $("#column-employee").val() == null ? 'Id' : $("#column-employee").val();
    var sort_order = $("#sort-order-employee").val();
    var data = {
        'sortBy': sort_order,
        'column': column,
    }

    $.ajax({
        type: 'GET',
        url: '/Payroll/employees/sort_employees/',
        data: data,
        dataType: 'json',
        success: function(data){
             $("#employee_table tbody").html(data.employee_table_records);
             $("#employee_pagination").html(data.employee_pagination);
        },
        error: function(data){
            console.log(data);
        }
    });

});
/*
--------------------------------------------------------
********************FOR LIMIT**************************
--------------------------------------------------------
*/

$("#record-limit-employee").change(function(e){
    var limit = $(this).val();
    var data = {'limit': limit};

    $.ajax({
        type: 'GET',
        url: '/Payroll/employees/record_limit_employees/',
        data: data,
        dataType: 'json',
        success: function(data){
            $("#employee_table tbody").html(data.employee_table_records);
            $("#employee_pagination").html(data.employee_pagination);
        },
        error: function(data){
            console.log(data);
        }

    });
});
/*
--------------------------------------------------------
********************FOR SEARCH**************************
--------------------------------------------------------
*/

function searchResultsEmployee(){
    var searchVal = $("#search-employee").val();

    var data = {
        'search_text': searchVal
    };

    $.ajax({
        type: 'GET',
        url: '/Payroll/employees/search_employees/',
        data: data,
        dataType: 'json',
        success: function(data){
            $("#employee_table tbody").html(data.employee_table_records);
            $("#employee_pagination").html(data.employee_pagination);
        },
        error: function(data){
            console.log(data);
        }
    });
}

$(".btn-search-employee").click(function(e){
    e.preventDefault();
     var searchVal = $("#search-employee").val();
     if(searchVal.trim() === ""){

     }else{
        searchResultsEmployee();
     }
});

$("#form-search-employee").submit(function(e){
    e.preventDefault();
   var searchVal = $("#search-employee").val();
     if(searchVal.trim() === ""){

     }else{
        searchResultsEmployee();
     }
});

$("#search-employee").keyup(function(e){
    if($("#search-employee").val().length <= 0){
        searchResultsEmployee();
    }
});
/*
--------------------------------------------------------
********************FOR PAGINATION**********************
--------------------------------------------------------
*/

$("#employee_pagination").on('click', '.page-link', function(e){
    var currentPage = $(this).text();
    var href = $(this).attr('href');

    $.ajax({
        type: 'GET',
        url: '/Payroll/employees/paging_employees/',
        dataType: 'json',
        success: function(data){
            $("#employee_table tbody").html(data.employee_table_records);
            $("#employee_pagination").html(data.employee_pagination);
        },
        error: function(data){
            console.log(data);
        }
    });

    return false;

});
//=======================================================================

var ShowEmployeeForm = function(e){
    e.preventDefault();
    var button = $(this);
    var searchVal = $("#search-employee").val();

    $.ajax({
        url: button.attr("data-url"),
        type: 'GET',
        data: {'search_text': searchVal},
        dataType: 'json',
        beforeSend: function(){
            $("#modal-form").modal('show');
        },
        success: function(data){
            $("#modal-form .modal-content").html(data.html_form);

        }
    });
}





var SaveEmployeeForm = function(e){
    e.preventDefault();

    var form = $(this);
    var formData = false;

    if(window.FormData){
        formData = new FormData(form[0]); //When we create instance of FormData we pass form[0] instead form. It's mean actual form element, but not jQuery selector.
    }

    $.ajax({
        url: form.attr("data-url"),
        data: formData ? formData : form.serialize(),
        cache: false,
        contentType: false,
        processData: false,
        type: form.attr("method"),
        dataType: 'json',
        success: function(data){
            if(data.form_is_valid){
                $("#modal-form").modal('hide');
                $("#employee_table tbody").html(data.employee_table_records);
                $("#employee_pagination").html(data.employee_pagination);
            }else{
                $("#modal-form .modal-content").html(data.html_form);
            }
        }
    });

    return false;
}
$("#employee_table").on('click', '.show-edit-employee-form', ShowEmployeeForm);
$("#modal-form").on("submit", ".employee-update-form", SaveEmployeeForm);

$("#employee_table").on('click', '.show-delete-employee-form', ShowEmployeeForm);
$("#modal-form").on("submit", ".employee-update-form", SaveEmployeeForm);
/*
--------------------------------------------------------
********************FOR BILL CREATION*******************
--------------------------------------------------------
*/

var ShowPayrollForm = function(e){
    e.preventDefault();
    var button = $(this);

    $.ajax({
        url: button.attr("data-url"),
        type: 'GET',
        dataType: 'json',
        beforeSend: function(){
            $("#modal-form").modal('show');
        },
        success: function(data){
            $("#modal-form .modal-content").html(data.html_form);
            $("#payroll_cut_off_period_from").datepicker({
               uiLibrary: 'bootstrap4',
               iconsLibrary: 'fontawesome',
               format: 'mmm dd yyyy',
            });
            $("#payroll_cut_off_period_to").datepicker({
               uiLibrary: 'bootstrap4',
               iconsLibrary: 'fontawesome',
               format: 'mmm dd yyyy',
            });
            $("#payroll_date").datepicker({
               uiLibrary: 'bootstrap4',
               iconsLibrary: 'fontawesome',
               format: 'mmm dd yyyy',
            });

            $("#id_basic_pay, #id_allowance, #id_overtime_pay, #id_legal_holiday, #id_special_holiday, #id_late_or_absences, #id_salary_or_cash_advance, #id_sss_premiums, #id_philhealth_contribution, #id_pagibig_contribution, #id_withholding_tax, #id_pagibig_loan").keyup(function(e){
                    var basic_pay = (isNaN(parseFloat($("#id_basic_pay").val())) ? 0 : parseFloat($("#id_basic_pay").val()));
                    var allowance = (isNaN(parseFloat($("#id_allowance").val())) ? 0 : parseFloat($("#id_allowance").val()));
                    var overtime = (isNaN(parseFloat($("#id_overtime_pay").val())) ? 0 : parseFloat($("#id_overtime_pay").val()));
                    var legalHoliday = (isNaN(parseFloat($("#id_legal_holiday").val())) ? 0 : parseFloat($("#id_legal_holiday").val()));
                    var specialHoliday = (isNaN(parseFloat($("#id_special_holiday").val())) ? 0 : parseFloat($("#id_special_holiday").val()));
                    var lates = (isNaN(parseFloat($("#id_late_or_absences").val())) ? 0 : parseFloat($("#id_late_or_absences").val()));
                    var cashAdvance = (isNaN(parseFloat($("#id_salary_or_cash_advance").val())) ? 0 : parseFloat($("#id_salary_or_cash_advance").val()));

                    var grossPay = (basic_pay + allowance + overtime + legalHoliday + specialHoliday) - (lates + cashAdvance);

    //                deductions

                    var sss = (isNaN(parseFloat($("#id_sss_premiums").val())) ? 0 : parseFloat($("#id_sss_premiums").val()));
                    var philhealth = (isNaN(parseFloat($("#id_philhealth_contribution").val())) ? 0 : parseFloat($("#id_philhealth_contribution").val()));
                    var pagibig = (isNaN(parseFloat($("#id_pagibig_contribution").val())) ? 0 : parseFloat($("#id_pagibig_contribution").val()));
                    var withholdingTax = (isNaN(parseFloat($("#id_withholding_tax").val())) ? 0 : parseFloat($("#id_withholding_tax").val()));
                    var pagibigLoan = (isNaN(parseFloat($("#id_pagibig_loan").val())) ? 0 : parseFloat($("#id_pagibig_loan").val()));

                    var totalDeduction = (sss + philhealth + pagibig + withholdingTax + pagibigLoan)

                    var netPay = grossPay - totalDeduction;


                    $("#id_gross_pay").val(grossPay);
                    $("#id_total_deduction").val(totalDeduction);
                    $("#id_net_pay").val(netPay);
           });

        }
    });
}




var SavePayrollForm = function(){
    var form = $(this);

    $.ajax({
        url: form.attr("data-url"),
        data: form.serialize(),
        cache: false,
        type: form.attr("method"),
        dataType: 'json',
        success: function(data){
            if(data.form_is_valid){
                $("#modal-form").modal("hide");
            }else{
                $("#modal-form .modal-content").html(data.html_form);
            }
        }
    });

    return false;
}
$("#employee_table").on('click', '.show-payroll-employee-form', ShowPayrollForm);
$("#modal-form").on("submit", ".employee-payroll-form", SavePayrollForm);


var ShowPayrollHistoryForm = function(e){
    e.preventDefault();
    var button = $(this);

    $.ajax({
        url: button.attr("data-url"),
        type: 'GET',
        dataType: 'json',
        beforeSend: function(){
            $("#modal-form-payroll-history").modal('show');
        },
        success: function(data){
            $("#modal-form-payroll-history .modal-content").html(data.html_form);

        }
    });
}
$("#employee_table").on('click', '.show-payroll-history-employee-form', ShowPayrollHistoryForm);



var ShowPayrollHistoryDetailForm = function(e){
    e.preventDefault();
    var button = $(this);

    $.ajax({
        url: button.attr("data-url"),
        type: 'GET',
        dataType: 'json',
        beforeSend: function(){
            $("#modal-form-payroll-history-detail").modal('show');
        },
        success: function(data){
            $("#modal-form-payroll-history-detail .modal-content").html(data.html_form);

        }
    });
}


$(document).on('click', '.show-payroll-history-employee-detail-form', ShowPayrollHistoryDetailForm);

//client side



var ShowClientEmployeePayrollDetailForm = function(e){
    e.preventDefault();
    var button = $(this);

    $.ajax({
        url: button.attr("data-url"),
        type: 'GET',
        dataType: 'json',
        beforeSend: function(){
            $("#modal-form-client-employee-payroll-detail").modal('show');
        },
        success: function(data){
            $("#modal-form-client-employee-payroll-detail .modal-content").html(data.html_form);

        }
    });
}
$("#table-client-employee-payroll-history").on("click", ".show-client-employee-payroll-form", ShowClientEmployeePayrollDetailForm);



});