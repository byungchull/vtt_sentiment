1. getSteamData.py :
   http://store.steampowered.com/search/?tags=1742&page= (현재 62페이지까지 있음)

   URL 에서 tags=1742 => rich story 태그에 해당하는 코드값
   각 페이지의 HTML 태그를 보면 <span class="title">Total War: WARHAMMER II</span> 와 같이 게임 제목 코드 부분에
   대해서 parsing을 통해서 게임 제목을 가져온다. 호출하는 시점에 따라 게임 순위가 계속 바뀜

   Thread 방식으로 실행, BeautifulSoup을 설치해야 함
   실행 결과에 해당하는 게임명은 SteamGameList.txt 파일에 저장 (1줄에 1게임명)

   참조코드 : http://bab2min.tistory.com/555

2. getWikiPlot.py :
   SteamGameList.txt 파일에서 게임 목록을 읽어서
   https://en.wikipedia.org/w/index.php?fulltext=&title=Special%3ASearch&go=Go&search=게임명 으로 HTML 크롤링

   크롤링 내용을 wikiLogSearch.txt 파일에 통째로 저장한다.

   URL은 http://en.wikipedia.org 페이지에서 상단의 검색 기능과 동일하다.

   게임명에서 일부 특수문자만 제거하고 (™, ®) 크롤링해서 최대 1545개 중 971개 검색 결과가 없음 (검색된 574개)

   위키피디아에서 검색할 때 게임이 아닌 검색 결과를 가져오는 경우도 있음 (게임명 : Plug & Play)

   검색된 574개 중에서 Plot 또는 Synopsis가 있는 위키피디아 페이지의 개수는 295개

   Plot 텍스트는 wikiPlotText.txt 파일에 게임명과 함께 저장   
   
   저장된 내용에서 [edit] 로 검색해서 sub title에 해당하는 줄 삭제 (Theories, story, Alternate endings, Road to Gehenna, Endings 등)

   참조링크 표시 \[[0-9]*\]   \[[a-z]*\]   \[+.*\]+  정규식에 대해서 수동으로 제거후에 wikiPlotText_m.txt로 저장

