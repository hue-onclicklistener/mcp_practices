from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base

import os
import shutil

mcp = FastMCP("linux-command")

@mcp.tool()
async def mkdir(dir_name: str) -> str:
    """create a direcotry on current working directory of server
    
    Args:
        dir_name: a directory name you want to create
    """
    current_path = os.getcwd()
    full_path = os.path.join(current_path, dir_name)
    try:
        os.makedirs(full_path)
        return(f"디렉터리 '{full_path}'가 성공적으로 생성되었습니다.")
    except FileExistsError:
        return(f"디렉터리 '{full_path}'는 이미 존재합니다.")
    except OSError as e:
        return(f"디렉터리 '{full_path}' 생성 중 오류 발생: {e}")

@mcp.tool()
async def rmdir(dir_name: str) -> str:
    """
    현재 작업 디렉터리에서 지정된 이름의 디렉터리를 삭제합니다.
    디렉터리 내에 내용물이 있어도 강제로 삭제합니다.

    Args:
        dir_name (str): 삭제할 디렉터리의 이름입니다.

    Returns:
        str: 작업 결과 메시지.
    """
    current_path = os.getcwd()
    full_path = os.path.join(current_path, dir_name)

    try:
        # 1. 경로 존재 여부 확인
        if not os.path.exists(full_path):
            return f"오류: 삭제할 디렉터리 '{full_path}'를 찾을 수 없습니다."
        
        # 2. 해당 경로가 디렉터리인지 확인
        if not os.path.isdir(full_path):
            return f"오류: '{full_path}'는 디렉터리가 아닙니다. 파일은 삭제할 수 없습니다."

        # 3. 디렉터리와 그 내용 강제 삭제
        shutil.rmtree(full_path)
        return f"디렉터리 '{full_path}'와 그 내용이 성공적으로 삭제되었습니다."

    except OSError as e:
        # shutil.rmtree()에서 권한 문제 등으로 오류 발생 가능
        return f"디렉터리 '{full_path}' 삭제 중 오류 발생: {e}"
    except Exception as e:
        # 기타 예외 처리
        return f"디렉터리 '{full_path}' 삭제 중 예상치 못한 오류 발생: {e}"
    
@mcp.prompt()
def default_prompt(message: str) -> list[base.Message]:
    return [
        base.AssistantMessage(
            "You are a helpful linux command executor. \n"
            "Please clearly organize and return the results of linux command execution."
        ),
        base.UserMessage(message),
    ]
    

if __name__ == "__main__":
    mcp.run(transport='stdio')
