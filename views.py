# archive/views.py
from django.shortcuts import render, redirect, get_object_or_404 # แก้ไขการสะกด get_object_or_404
from .models import Document
from django.db.models import Q # เพิ่มการ import Q เข้ามาด้านบนสุดของไฟล์

def home_view(request):
    # หน้าแรก: แสดงเฉพาะ 3 รายการล่าสุดเพื่อแนะนำแอป
    latest_results = Document.objects.all().order_by('-upload_date')[:3]
    return render(request, 'index.html', {'results': latest_results})

def list_view(request):
    # 1. ดึงค่าจากช่องค้นหา (q) และหมวดหมู่ (cat)
    query_name = request.GET.get('q')
    query_cat = request.GET.get('cat')
    
    # 2. เริ่มต้นดึงข้อมูลทั้งหมด
    results = Document.objects.all().order_by('-upload_date')

    # 3. ส่วนของการค้นหา (Logic ที่ทำให้พิมพ์แล้วเจอ)
    if query_name:
        # ใช้ Q เพื่อให้ค้นหาได้ทั้งในชื่อ (title) หรือ รหัสวิชา (subject_code)
        results = results.filter(
            Q(title__icontains=query_name) | 
            Q(subject_code__icontains=query_name)
        )
    
    # 4. ส่วนของการกรองตามหมวดหมู่ (สรุป/ข้อสอบ)
    if query_cat:
        results = results.filter(category=query_cat)

    return render(request, 'list.html', {'results': results})

# ฟังก์ชันเพิ่มข้อมูล
def add_view(request):
    if request.method == "POST":
        file_data = request.FILES.get('file_upload') 
        
        Document.objects.create(
            subject_code=request.POST.get('subject_code'),
            title=request.POST.get('title'),
            category=request.POST.get('category'),
            subject_category=request.POST.get('subject_category'), # เพิ่มบรรทัดนี้
            description=request.POST.get('description'),
            file=file_data
        )
        return redirect('archive:list') # เปลี่ยนเป็นไปหน้า list เพื่อดูผลลัพธ์
    return render(request, 'form.html')

# ฟังก์ชันลบข้อมูล (พร้อมระบบแจ้งเตือนตามขอบเขตงาน)
def delete_view(request, pk):
    # ดึงข้อมูลที่ต้องการลบ ถ้าไม่เจอจะส่งหน้า 404
    obj = get_object_or_404(Document, pk=pk)
    
    if request.method == "POST":
        obj.delete() # คำสั่งลบข้อมูลออกจากฐานข้อมูล
        return redirect('archive:home') # ลบเสร็จแล้วกลับหน้าแรก
        
    # ถ้ายังไม่ได้กดปุ่มยืนยัน (GET) ให้ไปหน้ายืนยันก่อน
    return render(request, 'delete_confirm.html', {'object': obj})
