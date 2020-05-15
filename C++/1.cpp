/**══════════════════════════════════╗
* 作    者：泡泡
* 邮    箱：pop929@qq.com
*═══════════════════════════════════╣
* 创建时间：2020-5-14  18：40
* 功能描述：根据图片分辨率的宽高比来将图像进行分类
*
*═══════════════════════════════════╣
* 结束时间:
*═══════════════════════════════════╝
*/

#include <iostream>
#include <fstream>
#include <string>
#include<Windows.h>
#include<gdiplus.h>
#include<vector>
#include<mutex>
#include<thread>
#include<filesystem>
#pragma comment(lib,"gdiplus.lib")

using namespace std;
namespace fs = std::filesystem;
using namespace Gdiplus;

void kit_1();
void find(vector<fs::path>& filelist, int tn, ofstream& of,bool begin_dir);
void read_files(std::vector<wstring>& filepaths, std::vector<wstring>& filenames, const wstring& directory);
int array_sum(int* array,int len);
void show_kit1(int file_total, ofstream& of, ULONG_PTR& gdiplustoken);
int *total;//执行过的文件夹的文件总数
int *file_j;//执行过的总文件数
int *file_i; //执行过的文件数(开始目录下的)
int *ok;//线程执行情况 完成后+1
int thread_sum = thread::hardware_concurrency();
mutex er_txt;

void text()
{
    
}

int main()
{
    kit_1();
    system("pause");
}

void kit_1()
{
    //初始化gdiplus
    GdiplusStartupInput m_gdiplusStartupInput;
    ULONG_PTR gdiplustoken;
    GdiplusStartup(&gdiplustoken, &m_gdiplusStartupInput, NULL);
    ofstream of("error.txt",ios::out);
    fs::create_directory(L"square");
    fs::create_directory(L"vertical");
    fs::create_directory(L"cross");

    total = new int[thread_sum];
    file_j = new int[thread_sum];
    file_i = new int[thread_sum];
    ok = new int[thread_sum];
    for (int i = 0; i < thread_sum; i++) {
        total[i] = 0;
        file_j[i] = 0;
        file_i[i] = 0;
        ok[i] = 0;
    }
    vector<vector<fs::path> > filelist(thread_sum);
    
    fs::directory_iterator di("./");
    int p = 0;
    for (auto item : di) {
        if (item.path().filename().wstring()[0] == L'.')
            continue;
        p %= thread_sum;
        filelist[p].push_back(item.path().filename());
        p++;
        //cout << item.path() << endl;
    }
    
    thread* ts = new thread[thread_sum];
    for (int i = 0; i < thread_sum; i++) {
        ts[i] = thread(find, ref(filelist[i]), i, ref(of), true);
    }

    int filetotal = 0; //开始目录的文件总数
    for (int i = 0; i < filelist.size(); i++) {
        filetotal += filelist[i].size();
    }
    show_kit1(filetotal, of, gdiplustoken);
    for (int i = 0; i < thread_sum; i++) {
        ts[i].join();
    }
    delete[] total;
    delete[] file_i;
    delete[] file_j;
    delete[] ok;
    delete[] ts;
}

bool is_target_directory(const fs::path& item)
{
    if (item.filename().wstring() == L"vertical") return true;
    if (item.filename().wstring() == L"cross") return true;
    if (item.filename().wstring() == L"square") return true;
    return false;
}

bool is_pictrue(fs::path& item)
{
    if (item.extension().wstring() == L".jpg") return true;
    if (item.extension().wstring() == L".png") return true;
    if (item.extension().wstring() == L".jpeg") return true;
    return false;
}

void find(vector<fs::path>& filelist, int tn, ofstream& of,bool is_begin_dir)
{
    total[tn] += filelist.size();
    fs::directory_iterator* di;
    double ratio;
    wstring dst;
    for (auto item : filelist) {
        ++file_j[tn];
        //如果是目录
        //cout << "' ---item  is " << item << endl;
        if (fs::is_directory(item)) {
            if (is_target_directory(item.filename())) {
                ++file_i[tn];
                continue;
            }
            vector<fs::path> file_list;
            if (is_begin_dir)
                file_i[tn]++;
            di = new fs::directory_iterator(item);
            //cout << "item:" << item << "----------\n";
            for (auto item2 : *di) {
                if (item2.path().filename().wstring()[0] == L'.')
                    continue;
                file_list.push_back(item2.path());
                //cout << item2.path().filename() << endl;
            }
            delete di;
            find(file_list,tn,of, false);
        }
        //如果是图片
        if (is_pictrue(item)) {
            //计算图片长宽比函数
            Bitmap* bmp = new Bitmap(item.filename().c_str());
            ratio = bmp->GetWidth() / double(bmp->GetHeight());
            delete bmp;
            if (ratio < 0.8) //竖的
                dst = L"./vertical/" + item.filename().wstring();
            else if (ratio > 1.3) //横的
                dst = L"./cross/" + item.filename().wstring();
            else //正的
                dst = L"./square/" + item.filename().wstring();
            //rename(item, dst);
            if (MoveFile(item.wstring().c_str(), dst.c_str()) == 0) {
                //cout << item << " move failed .... \n";
                er_txt.lock();
                of << item.string() << endl;
                er_txt.unlock();
            }
        }
    }

    if (is_begin_dir)
        ok[tn] = 1;
    //cout << "----------------ok[" << tn << "]:  " << ok[tn] << endl;
}

//读取文件夹下面的所有文件（不包括目录下的文件夹里面的文件）
void read_files(std::vector<wstring>& filepaths, std::vector<wstring>& filenames, const wstring& directory)
{
    HANDLE dir;
    WIN32_FIND_DATA file_data;
    cout << "into read_files" << endl;
    if ((dir = FindFirstFile(directory.c_str(), &file_data)) == INVALID_HANDLE_VALUE)
        return; //No files found 

    do {
        const wstring file_name = file_data.cFileName;
        const wstring file_path = directory + L"/" + file_name;
        const bool is_directory = (file_data.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY) != 0;

        if (file_name[0] == '.')
            continue;

        if (is_directory)
            continue;

        filepaths.push_back(file_path);
        cout << "add path:" << file_path.c_str() << endl;
        filenames.push_back(file_name);
    } while (FindNextFile(dir, &file_data));

    FindClose(dir);
}

//数组之和
int array_sum(int* array,int len)
{
    if (len < 1) return 0;
    int sum = 0;
    //cout << "len is:" << len << endl;
    for (int i = 0; i < len;  i++) {
        sum += array[i];
        //cout << "array[i]:" << array[i] << endl;
    }
    //cout << "array_sum is " << sum << endl;
    return sum;
}

void show_kit1(int file_total, ofstream& of, ULONG_PTR& gdiplustoken)
{
    int t = 0;
    while (array_sum(ok, thread_sum) != thread_sum) {
        cout << "total progress:" << array_sum(file_i, thread_sum) << "/" << file_total << "  ----  folder progress:"
            << array_sum(file_j, thread_sum) << '/' << array_sum(total, thread_sum) << "  -- take time:" << t * 0.5 << "s \n";
        Sleep(500);
        ++t;
    }
    cout << "\n----------picture move success!!!" << endl;
    of.close();
    GdiplusShutdown(gdiplustoken);//关闭gdi
}


// WCHAR 转换为 std::string
string WCHAR2String(LPCWSTR pwszSrc)
{
    int nLen = WideCharToMultiByte(CP_ACP, 0, pwszSrc, -1, NULL, 0, NULL, NULL);
    if (nLen <= 0)
        return std::string("");

    char* pszDst = new char[nLen];
    if (NULL == pszDst)
        return string("");

    WideCharToMultiByte(CP_ACP, 0, pwszSrc, -1, pszDst, nLen, NULL, NULL);
    pszDst[nLen - 1] = 0;
    string temp(pszDst);
    delete[] pszDst;
    return temp;
}