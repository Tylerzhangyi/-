// 存储学生数据的变量
let studentData = {};

// 页面加载完成后初始化
$(document).ready(function() {
    // 使用jQuery AJAX获取学生数据
    $.ajax({
        url: '/student',
        method: 'GET',
        dataType: 'json',
        success: function(response) {
            console.log('成功获取学生数据:', response);
            
            // 存储数据
            studentData = response.data;
            
            // 动态创建学生span元素
            createStudentSpans();
            
            // 绑定点击事件
            bindClickEvents();
        },
        error: function(xhr, status, error) {
            console.error('获取学生数据失败:', error);
            $('.content h2').text('数据加载失败');
        }
    });
});

// 动态创建学生span元素
function createStudentSpans() {
    const studentsContainer = $('.students');
    
    // 清空容器
    studentsContainer.empty();
    
    // 遍历数据创建span
    studentData.forEach(function(student) {
        const span = $('<span>')
            .addClass('student')
            .attr('data-student', student.id)
            .text(student.name);
        
        studentsContainer.append(span);
    });
}

// 绑定点击事件
function bindClickEvents() {
    $('.student').on('click', function() {
        const studentId = $(this).attr('data-student');
        
        // 查找对应的学生信息
        const student = studentData.find(s => s.id === studentId);
        
        if (student) {
            // 更新内容
            $('.content').html(`<div class="student-info "><h4>${student.info}</h4></div>`);
        }
    });
}