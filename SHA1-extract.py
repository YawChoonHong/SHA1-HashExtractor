#include <iostream>
#include <fstream>
#include <filesystem>
#include <string>
#include <vector>
#include <openssl/sha.h> // Make sure you have OpenSSL installed
#include <zip.h> // Miniz or any zip library you prefer
#include <archive.h>
#include <archive_entry.h>

namespace fs = std::filesystem;

struct FileInfo {
    std::string path;
    std::string name;
    std::string hash;
};

std::string sha1_hash(const std::string& file_path) {
    unsigned char hash[SHA_DIGEST_LENGTH];
    FILE* file = fopen(file_path.c_str(), "rb");
    if (!file) return "File not found.";

    SHA_CTX sha1;
    SHA1_Init(&sha1);
    char buffer[4096];
    size_t bytesRead;

    while ((bytesRead = fread(buffer, 1, sizeof(buffer), file)) != 0) {
        SHA1_Update(&sha1, buffer, bytesRead);
    }
    SHA1_Final(hash, &sha1);
    fclose(file);

    std::string hashString;
    for (int i = 0; i < SHA_DIGEST_LENGTH; i++) {
        hashString += sprintf("%02x", hash[i]);
    }
    return hashString;
}

void write_hash_to_excel(const std::vector<FileInfo>& files_info, const std::string& excel_file) {
    // Use a library like libxlsxwriter to write to an Excel file
    // Placeholder for Excel writing logic
}

void write_hash_to_text(const std::vector<FileInfo>& files_info, const std::string& text_file) {
    std::ofstream out(text_file);
    out << "File Count | File Path | File Name | SHA-1 Hash\n";
    out << "---------------------------------------------------\n";
    for (size_t i = 0; i < files_info.size(); i++) {
        out << (i + 1) << " | " << files_info[i].path << " | " << files_info[i].name << " | " << files_info[i].hash << "\n";
    }
    out.close();
}

void write_hash_only(const std::vector<FileInfo>& files_info, const std::string& simple_text_file) {
    std::ofstream out(simple_text_file);
    for (const auto& file_info : files_info) {
        out << file_info.hash << "\n";
    }
    out.close();
}

void process_folder(const std::string& folder_path, const std::string& excel_file, const std::string& text_file, const std::string& simple_text_file) {
    std::vector<FileInfo> files_info;

    for (const auto& entry : fs::directory_iterator(folder_path)) {
        if (fs::is_regular_file(entry)) {
            FileInfo file_info;
            file_info.path = entry.path().string();
            file_info.name = entry.path().filename().string();
            file_info.hash = sha1_hash(file_info.path);
            files_info.push_back(file_info);
        } else if (entry.path().extension() == ".zip") {
            // Handle ZIP extraction (using miniz or similar library)
            // Placeholder for ZIP extraction and hash calculation
        } else if (entry.path().extension() == ".rar") {
            // Handle RAR extraction (using libarchive or similar library)
            // Placeholder for RAR extraction and hash calculation
        }
    }

    if (!excel_file.empty()) write_hash_to_excel(files_info, excel_file);
    if (!text_file.empty()) write_hash_to_text(files_info, text_file);
    if (!simple_text_file.empty()) write_hash_only(files_info, simple_text_file);
}

int main() {
    std::string folder_path = "path_to_folder"; // Set this to your target folder
    std::string excel_file = "file_hashes.xlsx";
    std::string text_file = "file_hashes.txt";
    std::string simple_text_file = "hashes_only.txt";

    process_folder(folder_path, excel_file, text_file, simple_text_file);
    std::cout << "Hashes have been written to the selected formats." << std::endl;

    return 0;
}
