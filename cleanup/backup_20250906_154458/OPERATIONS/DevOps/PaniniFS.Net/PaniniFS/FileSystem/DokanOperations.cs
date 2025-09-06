using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Security.AccessControl;
using System.Text;
using System.Threading.Tasks;
using DokanNet;
using DokanNet.Logging;
using PaniniFS;
using FileAccess = DokanNet.FileAccess;

namespace Panini.FileSystem
{
    class DokanOperations : IDokanOperations
    {
        private static readonly log4net.ILog log =
    log4net.LogManager.GetLogger(System.Reflection.MethodBase.GetCurrentMethod().DeclaringType);

        /// <summary>
        /// Receipt of this request indicates that the last handle for a file object that is associated 
        /// with the target device object has been closed (but, due to outstanding I/O requests, 
        /// might not have been released).
        ///
        /// Cleanup is requested before CloseFile is called.
        /// 
        /// When IDokanFileInfo.DeleteOnClose is true, you must delete the file in Cleanup.Refer to 
        /// DeleteFile and DeleteDirectory for explanation.
        /// 
        /// </summary>
        /// <param name="fileName">File path requested by the Kernel on the FileSystem.</param>
        /// <param name="info">	An IDokanFileInfo with information about the file or directory.</param>
        public void Cleanup(string fileName, IDokanFileInfo info)
        {
            // TODO  implement Cleanup
            
        }

        /// <summary>
        /// CloseFile is called at the end of the life of the context.
        /// 
        /// Receipt of this request indicates that the last handle of the file object that is associated 
        /// with the target device object has been closed and released.All outstanding I/O requests have 
        /// been completed or canceled.
        /// 
        /// CloseFile is requested after Cleanup is called.
        /// 
        /// Remainings in IDokanFileInfo.Context has to be cleared before return.
        /// </summary>
        /// <param name="fileName">File path requested by the Kernel on the FileSystem.</param>
        /// <param name="info">An IDokanFileInfo with information about the file or directory.</param>
        public void CloseFile(string fileName, IDokanFileInfo info)
        {
            // TODO  implement CloseFile
        }

        #region Create/Delete File
        /// <summary>
        /// CreateFile is called each time a request is made on a file system object.
        ///
        /// In case mode is FileMode.OpenOrCreate and FileMode.Create and CreateFile are successfully 
        /// opening a already existing file, you have to return DokanResult.AlreadyExists instead of 
        /// NtStatus.Success.
        ///
        /// If the file is a directory, CreateFile is also called. In this case, CreateFile should 
        /// return NtStatus.Success when that directory can be opened and IDokanFileInfo.IsDirectory
        /// must be set to true. On the other hand, if IDokanFileInfo.IsDirectory is set to true but 
        /// the path target a file, you need to return DokanResult.NotADirectory
        ///
        /// IDokanFileInfo.Context can be used to store data (like FileStream) that can be retrieved 
        /// in all other request related to the context.
        /// </summary>
        /// <param name="fileName">File path requested by the Kernel on the FileSystem.</param>
        /// <param name="access">A FileAccess with permissions for file or directory.</param>
        /// <param name="share">Type of share access to other threads, which is specified as FileShare.
        /// None or any combination of FileShare. Device and intermediate drivers usually set ShareAccess 
        /// to zero, which gives the caller exclusive access to the open file.</param>
        /// <param name="mode">Specifies how the operating system should open a file. See FileMode 
        /// Enumeration (MSDN).</param>
        /// <param name="options">	Represents advanced options for creating a FileStream object. See 
        /// FileOptions Enumeration (MSDN).
        /// https://msdn.microsoft.com/en-us/library/system.io.filemode(v=vs.110).aspx</param>
        /// <param name="attributes">	Provides attributes for files and directories. See FileAttributes 
        /// Enumeration (MSDN>.
        /// https://msdn.microsoft.com/en-us/library/system.io.fileoptions(v=vs.110).aspx</param>
        /// <param name="info">An IDokanFileInfo with information about the file or directory.</param>
        /// <returns>Return DokanResult.Success if file can be delete or NtStatus appropriate.</returns>
        public NtStatus CreateFile(string fileName, FileAccess access, FileShare share, FileMode mode, FileOptions options, FileAttributes attributes, IDokanFileInfo info)
        {
            // TODO  implement CreateFile
            return NtStatus.Success;
        }

        /// <summary>
        /// Check if it is possible to delete a file.
        ///
        /// You should NOT delete the file in DeleteFile, but instead you must only check whether you can 
        /// delete the file or not, and return NtStatus.Success(when you can delete it) or appropriate 
        /// error codes such as NtStatus.AccessDenied, NtStatus.ObjectNameNotFound.
        ///
        /// DeleteFile will also be called with IDokanFileInfo.DeleteOnClose set to false to notify the 
        /// driver when the file is no longer requested to be deleted.
        ///
        /// When you return NtStatus.Success, you get a Cleanup call afterwards with 
        /// IDokanFileInfo.DeleteOnClose set to true and only then you have to actually delete the file 
        /// being closed.
        /// </summary>
        /// <param name="fileName">	File path requested by the Kernel on the FileSystem.</param>
        /// <param name="info">An IDokanFileInfo with information about the file or directory.</param>
        /// <returns>Return DokanResult.Success if file can be delete or NtStatus appropriate.</returns>
        public NtStatus DeleteFile(string fileName, IDokanFileInfo info)
        {
            // TODO  implement DeleteFile
            return NtStatus.Success;
        }
        #endregion
        /// <summary>
        /// Check if it is possible to delete a directory.
        ///
        /// You should NOT delete the file in DeleteDirectory, but instead you must only check whether 
        /// you can delete the file or not, and return NtStatus.Success(when you can delete it) or 
        /// appropriate error codes such as NtStatus.AccessDenied, NtStatus.ObjectPathNotFound, 
        /// NtStatus.ObjectNameNotFound.
        ///
        /// DeleteFile will also be called with IDokanFileInfo.DeleteOnClose set to false to notify the 
        /// driver when the file is no longer requested to be deleted.
        ///
        /// When you return NtStatus.Success, you get a Cleanup call afterwards with 
        /// IDokanFileInfo.DeleteOnClose set to true and only then you have to actually delete the 
        /// file being closed.
        /// </summary>
        /// <param name="fileName">File path requested by the Kernel on the FileSystem.</param>
        /// <param name="info">An IDokanFileInfo with information about the file or directory.</param>
        /// <returns>
        /// Return DokanResult.Success if file can be delete or NtStatus appropriate.</returns>
        public NtStatus DeleteDirectory(string fileName, IDokanFileInfo info)
        {
            // TODO  implement DeleteDirectory
            return NtStatus.Success;
        }

        /// <summary>
        /// List all files in the path requested
        /// FindFilesWithPattern is checking first.If it is not implemented or returns 
        /// NtStatus.NotImplemented, then FindFiles is called.
        /// </summary>
        /// <param name="fileName">File path requested by the Kernel on the FileSystem.</param>
        /// <param name="files">An IDokanFileInfo with information about the file or directory.</param>
        /// <param name="info">	An IDokanFileInfo with information about the file or directory.</param>
        /// <returns>NtStatus or DokanResult appropriate to the request result.</returns>
        public NtStatus FindFiles(string fileName, out IList<FileInformation> files, IDokanFileInfo info)
        {
            // TODO  implement FindFiles
            files = new List<FileInformation>();
            return NtStatus.Success;
        }

        /// <summary>
        /// Same as FindFiles but with a search pattern to filter the result.
        /// </summary>
        /// <param name="fileName">	Path requested by the Kernel on the FileSystem.</param>
        /// <param name="searchPattern">Search pattern</param>
        /// <param name="files">	A list of FileInformation to return.</param>
        /// <param name="info">An IDokanFileInfo with information about the file or directory.</param>
        /// <returns>NtStatus or DokanResult appropriate to the request result.</returns>
        public NtStatus FindFilesWithPattern(string fileName, string searchPattern, out IList<FileInformation> files, IDokanFileInfo info)
        {
            // TODO  implement FindFilesWithPattern
            files = new List<FileInformation>();
            return NtStatus.Success;
        }

        /// <summary>
        /// Retrieve all NTFS Streams informations on the file. This is only called if 
        /// DokanOptions.AltStream is enabled.
        ///
        /// For files, the first item in streams is information about the default data stream "::$DATA".
        /// </summary>
        /// <param name="fileName">File path requested by the Kernel on the FileSystem.</param>
        /// <param name="streams">List of FileInformation for each streams present on the file.</param>
        /// <param name="info">	An IDokanFileInfo with information about the file or directory.</param>
        /// <returns>Return NtStatus or DokanResult appropriate to the request result.</returns>
        public NtStatus FindStreams(string fileName, out IList<FileInformation> streams, IDokanFileInfo info)
        {
            // TODO  implement FindStreams
            streams = new List<FileInformation>();
            return NtStatus.Success;
        }

        /// <summary>
        /// Clears buffers for this context and causes any buffered data to be written to the file.
        /// </summary>
        /// <param name="fileName">	File path requested by the Kernel on the FileSystem.</param>
        /// <param name="info"></param>
        /// <returns>An IDokanFileInfo with information about the file or directory.</returns>
        public NtStatus FlushFileBuffers(string fileName, IDokanFileInfo info)
        {
            // TODO  implement FlushFileBuffers
            return NtStatus.Success;
        }

        /// <summary>
        /// Retrieves information about the amount of space that is available on a disk volume, which is 
        /// the total amount of space, the total amount of free space, and the total amount of free space 
        /// available to the user that is associated with the calling thread.
        ///
        /// Neither GetDiskFreeSpace nor GetVolumeInformation save the IDokanFileInfo.Context.Before these 
        /// methods are called, CreateFile may not be called. (ditto CloseFile and Cleanup).
        /// </summary>
        /// <param name="freeBytesAvailable">	Amount of available space.</param>
        /// <param name="totalNumberOfBytes">Total size of storage space.</param>
        /// <param name="totalNumberOfFreeBytes">	Amount of free space.</param>
        /// <param name="info">	An IDokanFileInfo with information about the file or directory.</param>
        /// <returns>NtStatus or DokanResult appropriate to the request result.</returns>
        public NtStatus GetDiskFreeSpace(out long freeBytesAvailable, out long totalNumberOfBytes, out long totalNumberOfFreeBytes, IDokanFileInfo info)
        {
            // TODO  implement GetDiskFreeSpace
            freeBytesAvailable = 0;
            totalNumberOfBytes = 0;
            totalNumberOfFreeBytes = 0;
            return NtStatus.Success;
        }

        /// <summary>
        /// Retrieves information about the file system and volume associated with the specified root directory.
        ///
        /// Neither GetVolumeInformation nor GetDiskFreeSpace save the IDokanFileInfo.Context.Before these 
        /// methods are called, CreateFile may not be called. (ditto CloseFile and Cleanup).
        ///
        /// FileSystemFeatures.ReadOnlyVolume is automatically added to the features if 
        /// DokanOptions.WriteProtection was specified when the volume was mounted.
        ///
        /// If NtStatus.NotImplemented is returned, the Dokan kernel driver use following settings by default:
        /// </summary>
        /// <param name="volumeLabel">	Volume name</param>
        /// <param name="features">	FileSystemFeatures with features enabled on the volume.</param>
        /// <param name="fileSystemName">The name of the specified volume.</param>
        /// <param name="maximumComponentLength">File name component that the specified file system supports.</param>
        /// <param name="info">An IDokanFileInfo with information about the file or directory.</param>
        /// <returns>NtStatus or DokanResult appropriate to the request result.</returns>
        public NtStatus GetVolumeInformation(out string volumeLabel, out FileSystemFeatures features, out string fileSystemName, out uint maximumComponentLength, IDokanFileInfo info)
        {
            // TODO  implement GetVolumeInformation
            volumeLabel = Program.configuration.VolumeLabel;

            features = 
                FileSystemFeatures.VolumeIsCompressed &
                FileSystemFeatures.UnicodeOnDisk &
                FileSystemFeatures.CasePreservedNames &
                FileSystemFeatures.CaseSensitiveSearch;
            fileSystemName = "PaniniFS";
            maximumComponentLength = UInt32.MaxValue; // 4GB
            return NtStatus.Success;
        }

        /// <summary>
        /// Move a file or directory to a new location.
        /// </summary>
        /// <param name="oldName">Path to the file to move.</param>
        /// <param name="newName">Path to the new location for the file.</param>
        /// <param name="replace">If the file should be replaced if it already exist a file with path newName .</param>
        /// <param name="info">An IDokanFileInfo with information about the file or directory.</param>
        /// <returns>NtStatus or DokanResult appropriate to the request result.</returns>
        public NtStatus MoveFile(string oldName, string newName, bool replace, IDokanFileInfo info)
        {
            // TODO  implement MoveFile
            return NtStatus.Success;
        }

        /// <summary>
        /// SetAllocationSize is used to truncate or extend a file.
        /// </summary>
        /// <param name="fileName">	File path requested by the Kernel on the FileSystem.</param>
        /// <param name="length">	File length to set</param>
        /// <param name="info">	An IDokanFileInfo with information about the file or directory.</param>
        /// <returns></returns>
        public NtStatus SetAllocationSize(string fileName, long length, IDokanFileInfo info)
        {
            // TODO  implement SetAllocationSize
            return NtStatus.Success;
        }

        /// <summary>
        /// SetEndOfFile is used to truncate or extend a file (physical file size).
        /// </summary>
        /// <param name="fileName">File path requested by the Kernel on the FileSystem.</param>
        /// <param name="length">File length to set</param>
        /// <param name="info">An IDokanFileInfo with information about the file or directory.</param>
        /// <returns></returns>
        public NtStatus SetEndOfFile(string fileName, long length, IDokanFileInfo info)
        {
            // TODO  implement SetEndOfFile
            return NtStatus.Success;
        }

        /// <summary>
        /// Get specific informations on a file.
        /// </summary>
        /// <param name="fileName">File path requested by the Kernel on the FileSystem.</param>
        /// <param name="fileInfo">FileInformation struct to fill</param>
        /// <param name="info">An IDokanFileInfo with information about the file or directory.</param>
        /// <returns></returns>
        #region Get ... Information Security
        public NtStatus GetFileInformation(string fileName, out FileInformation fileInfo, IDokanFileInfo info)
        {
            // TODO  implement GetFileInformation
            fileInfo = new FileInformation();
            return NtStatus.Success;
        }

        /// <summary>
        /// Get specified information about the security of a file or directory.
        ///
        /// If NtStatus.NotImplemented is returned, dokan library will handle the request by building a sddl of the current process user with authenticate user rights for context menu.
        /// </summary>
        /// <param name="fileName">File or directory name.</param>
        /// <param name="security">A FileSystemSecurity with security information to return.</param>
        /// <param name="sections">A AccessControlSections with access sections to return.</param>
        /// <param name="info">An IDokanFileInfo with information about the file or directory.</param>
        /// <returns></returns>
        public NtStatus GetFileSecurity(string fileName, out FileSystemSecurity security, AccessControlSections sections, IDokanFileInfo info)
        {
            // TODO  implement GetFileSecurity
            security = new DirectorySecurity(); // FileSecurity

            return NtStatus.Success;
        }
        #endregion
        #region Set ... Attributes Time Security

        /// <summary>
        /// Set file attributes on a specific file.
        ///
        /// SetFileAttributes and SetFileTime are called only if both of them are implemented.
        /// </summary>
        /// <param name="fileName">	File path requested by the Kernel on the FileSystem.</param>
        /// <param name="attributes">FileAttributes to set on file</param>
        /// <param name="info">An IDokanFileInfo with information about the file or directory.</param>
        /// <returns></returns>
        public NtStatus SetFileAttributes(string fileName, FileAttributes attributes, IDokanFileInfo info)
        {
            // TODO  implement SetFileAttributes
            return NtStatus.Success;
        }

        /// <summary>
        /// Sets the security of a file or directory object.
        /// </summary>
        /// <param name="fileName">File path requested by the Kernel on the FileSystem.</param>
        /// <param name="security">A FileSystemSecurity with security information to set.</param>
        /// <param name="sections">A AccessControlSections with access sections on which.</param>
        /// <param name="info">An IDokanFileInfo with information about the file or directory.</param>
        /// <returns>NtStatus or DokanResult appropriate to the request result.</returns>
        public NtStatus SetFileSecurity(string fileName, FileSystemSecurity security, AccessControlSections sections, IDokanFileInfo info)
        {
            // TODO  implement SetFileSecurity
            return NtStatus.Success;
        }

        /// <summary>
        /// Set file times on a specific file. If DateTime is null, this should not be updated.
        ///
        /// SetFileAttributes and SetFileTime are called only if both of them are implemented.
        /// </summary>
        /// <param name="fileName">	File or directory name.</param>
        /// <param name="creationTime">DateTime when the file was created.</param>
        /// <param name="lastAccessTime">	DateTime when the file was last accessed.</param>
        /// <param name="lastWriteTime">DateTime when the file was last written to.</param>
        /// <param name="info">	An IDokanFileInfo with information about the file or directory.</param>
        /// <returns>NtStatus or DokanResult appropriate to the request result.</returns>
        public NtStatus SetFileTime(string fileName, DateTime? creationTime, DateTime? lastAccessTime, DateTime? lastWriteTime, IDokanFileInfo info)
        {
            // TODO  implement SetFileTime
            return NtStatus.Success;
        }
        #endregion

        #region Lock/Unlock

        /// <summary>
        /// Lock file at a specific offset and data length. This is only used if DokanOptions.UserModeLock is enabled.
        /// </summary>
        /// <param name="fileName">	File path requested by the Kernel on the FileSystem.</param>
        /// <param name="offset">	Offset from where the lock has to be proceed.</param>
        /// <param name="length">	Data length to lock.</param>
        /// <param name="info">An IDokanFileInfo with information about the file or directory.</param>
        /// <returns>NtStatus or DokanResult appropriate to the request result.</returns>
        public NtStatus LockFile(string fileName, long offset, long length, IDokanFileInfo info)
        {
            // TODO  implement LockFile
            return NtStatus.Success;
        }

        /// <summary>
        /// Unlock file at a specific offset and data length. This is only used if DokanOptions.UserModeLock is enabled.
        /// </summary>
        /// <param name="fileName">File path requested by the Kernel on the FileSystem.</param>
        /// <param name="offset">Offset from where the unlock has to be proceed.</param>
        /// <param name="length">Data length to lock.</param>
        /// <param name="info">An IDokanFileInfo with information about the file or directory.</param>
        /// <returns>NtStatus or DokanResult appropriate to the request result.</returns>
        public NtStatus UnlockFile(string fileName, long offset, long length, IDokanFileInfo info)
        {
            // TODO  implement UnlockFile
            return NtStatus.Success;
        }
        #endregion

        #region Mounted/Unmounted

        /// <summary>
        /// Is called when Dokan succeed to mount the volume.
        /// </summary>
        /// <param name="info">	An IDokanFileInfo with information about the file or directory.</param>
        /// <returns>NtStatus or DokanResult appropriate to the request result.</returns>
        public NtStatus Mounted(IDokanFileInfo info)
        {
            // TODO  implement Mounted
            return NtStatus.Success;
        }

        /// <summary>
        /// Is called when Dokan is unmounting the volume.
        /// </summary>
        /// <param name="info">An IDokanFileInfo with information about the file or directory.</param>
        /// <returns>NtStatus or DokanResult appropriate to the request result.</returns>
        public NtStatus Unmounted(IDokanFileInfo info)
        {
            // TODO  implement Unmounted
            return NtStatus.Success;
        }
        #endregion

        #region Read/Write

        /// <summary>
        /// ReadFile callback on the file previously opened in CreateFile. It can be called by different 
        /// thread at the same time, therefor the read has to be thread safe.
        /// </summary>
        /// <param name="fileName">	File path requested by the Kernel on the FileSystem.</param>
        /// <param name="buffer">	Read buffer that has to be fill with the read result. The buffer size 
        /// depend of the read size requested by the kernel.</param>
        /// <param name="bytesRead">Total number of bytes that has been read.</param>
        /// <param name="offset">Offset from where the read has to be proceed.</param>
        /// <param name="info"></param>
        /// <returns>An IDokanFileInfo with information about the file or directory.</returns>
        public NtStatus ReadFile(string fileName, byte[] buffer, out int bytesRead, long offset, IDokanFileInfo info)
        {
            // TODO  implement ReadFile
            bytesRead = 0;
            return NtStatus.Success;
        }

        /// <summary>
        /// WriteFile callback on the file previously opened in CreateFile It can be called by different thread at the same time, therefor the write/context has to be thread safe.
        /// </summary>
        /// <param name="fileName">	File path requested by the Kernel on the FileSystem.</param>
        /// <param name="buffer">	Data that has to be written.</param>
        /// <param name="bytesWritten">Total number of bytes that has been write.</param>
        /// <param name="offset">	Offset from where the write has to be proceed.</param>
        /// <param name="info">	An IDokanFileInfo with information about the file or directory.</param>
        /// <returns>NtStatus or DokanResult appropriate to the request result.</returns>
        public NtStatus WriteFile(string fileName, byte[] buffer, out int bytesWritten, long offset, IDokanFileInfo info)
        { 
            // TODO  implement WriteFile
            bytesWritten = 0;
            return NtStatus.Success;
        }
        #endregion
    }
}
